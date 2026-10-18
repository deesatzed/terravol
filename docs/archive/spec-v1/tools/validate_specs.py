#!/usr/bin/env python3
"""Validate VOLTERRA specification fixtures, NOT the forecasting application.

Run from any directory:
  python /path/to/VOLTERRA_spec_v1/tools/validate_specs.py
Requires jsonschema. No network, model inference or market data is used.
"""
from __future__ import annotations
import copy
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:
    raise SystemExit('Install requirements-spec-validation.txt before running this package-only check.') from exc

ROOT = Path(__file__).resolve().parents[1]

def reject_constant(value: str) -> None:
    raise ValueError(f'Non-finite JSON number is not permitted: {value}')

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'), parse_constant=reject_constant)

def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def dt(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    check(result.tzinfo is not None, 'Timezone-aware timestamp required.')
    return result

def validate_schema(name: str, value: Any) -> None:
    contract = read_json(ROOT / 'schemas' / f'{name}.schema.json')
    Draft202012Validator.check_schema(contract)
    Draft202012Validator(contract, format_checker=FormatChecker()).validate(value)

def evidence_check(value: dict[str, Any], origin: str) -> None:
    validate_schema('evidence', value)
    check(dt(value['available_at']) <= dt(origin), 'Evidence was unavailable at the forecast origin.')
    if value['published_at'] is not None:
        check(dt(value['published_at']) <= dt(value['available_at']), 'A revision cannot be available before its recorded publication.')
    if value['availability_basis'] == 'live_observed':
        check(dt(value['ingested_at']) <= dt(origin), 'Live evidence was not received before origin.')
    if value['availability_basis'] == 'synthetic_fixture':
        check(value['synthetic'], 'Synthetic evidence cannot remove its synthetic flag.')
    if value['status'] == 'observed':
        check(value['value'] is not None, 'Observed numeric fixture requires a value.')

def forecast_check(value: dict[str, Any]) -> None:
    validate_schema('forecast', value)
    check(dt(value['issued_at']) >= dt(value['origin']), 'A forecast cannot be issued before origin.')
    check(not set(value['failed_model_ids']).intersection(value['actual_model_ids']), 'A failed model cannot receive credit as an actual producing model.')
    if value['failed_model_ids']:
        check(value['status'] != 'OK', 'Failure requires an explicit degraded/failed status in this minimal contract.')
    if value['status'] in ('OK', 'DEGRADED'):
        check(bool(value['actual_model_ids']) and bool(value['horizon_forecasts']), 'Successful forecast requires actual producer and horizon output.')
    horizons = value['horizon_forecasts']
    session_counts = [h['sessions'] for h in horizons]
    check(session_counts == sorted(set(session_counts)), 'Horizons must be unique and ascending.')
    for h in horizons:
        check(dt(h['target_start']) >= dt(value['origin']), 'Fixture target starts before forecast origin.')
        check(dt(h['target_end']) > dt(h['target_start']), 'Target interval must be positive.')
        vs, ss = h['variance_quantiles'], h['volatility_quantiles']
        for pairs in (vs, ss):
            levels = [p['level'] for p in pairs]
            numbers = [p['value'] for p in pairs]
            check(levels == sorted(set(levels)), 'Quantile levels must be unique and ascending.')
            check(numbers == sorted(numbers), 'Quantile values must be monotone.')
        check([p['level'] for p in vs] == [p['level'] for p in ss], 'Variance and volatility quantile levels differ.')
        for vp, sp in zip(vs, ss):
            expected = math.sqrt(h['annualization_sessions'] * vp['value'] / h['sessions'])
            check(math.isclose(sp['value'], expected, rel_tol=1e-9, abs_tol=1e-12), 'Variance-to-volatility units or transformation mismatch.')
        if h['variance_mean'] is None:
            check(bool(h['mean_unavailable_reason']), 'Missing mean requires an explicit reason.')
        if h['representation'].startswith('joint_'):
            check('joint_paths' in value['capabilities'] and bool(value['joint_path_ref']), 'Joint representation requires a path reference and capability.')
    if 'joint_paths' in value['capabilities']:
        check(bool(value['joint_path_ref']), 'Joint-path capability has no path artifact reference.')
        check(all(h['representation'].startswith('joint_') for h in horizons), 'Marginal-only output cannot claim joint paths in this minimal contract.')
    if 'path_episode_forecast' in value['capabilities']:
        check('joint_paths' in value['capabilities'], 'Path episode output requires joint paths.')
    episode = value['episode_forecast']
    if episode:
        required = 'joint_paths' if episode['method'] == 'joint_paths' else 'validated_survival_head'
        check(required in value['capabilities'], 'Episode output lacks the required supported capability.')
    # Artifact existence, actual joint dependence, real sampling, calendars and
    # calibration need future application tests. A reference string proves none of these.

def graph_check(value: dict[str, Any]) -> None:
    validate_schema('graph', value)
    nodes = {n['node_id']: n for n in value['nodes']}
    check(len(nodes) == len(value['nodes']), 'Duplicate graph node IDs.')
    adjacency: dict[str, list[str]] = {key: [] for key in nodes}
    edge_pairs = set()
    for edge in value['edges']:
        check(edge['source'] in nodes and edge['target'] in nodes, 'Graph edge references an unknown node.')
        edge_pairs.add((edge['source'], edge['target']))
        if edge['lag_sessions'] == 0:
            adjacency[edge['source']].append(edge['target'])
    visiting, done = set(), set()
    def visit(key: str) -> None:
        check(key not in visiting, 'Instantaneous graph cycle.')
        if key in done:
            return
        visiting.add(key)
        for child in adjacency[key]:
            visit(child)
        visiting.remove(key); done.add(key)
    for key in nodes:
        visit(key)
    for node in nodes.values():
        lower, upper = node['support']['lower'], node['support']['upper']
        check(lower is None or upper is None or lower <= upper, 'Invalid support bounds.')
        dist = node['distribution']; family, params = dist['family'], dist['parameters']
        for item in params.values():
            if isinstance(item, dict):
                check(item['node_ref'] in nodes, 'Unknown distribution parameter node.')
                check((item['node_ref'],node['node_id']) in edge_pairs, 'Parameter reference has no declared dependency edge.')
        if family == 'beta':
            check(set(params) == {'alpha','beta'}, 'Beta requires alpha and beta.')
            check(all(isinstance(params[k], (int,float)) and params[k] > 0 for k in ('alpha','beta')), 'Invalid numeric beta parameters in fixture subset.')
            check(lower == 0 and upper == 1, 'Beta support must be [0,1].')
        elif family == 'bernoulli':
            check(set(params) == {'p'}, 'Bernoulli requires p.')
            p = params['p']
            if isinstance(p, dict):
                parent = nodes[p['node_ref']]['support']
                check(parent['lower'] == 0 and parent['upper'] == 1, 'Bernoulli probability parent requires [0,1] support.')
            else:
                check(0 <= p <= 1, 'Bernoulli probability outside [0,1].')
            check(lower == 0 and upper == 1, 'Bernoulli support must be [0,1].')
        elif family == 'student_t':
            check(isinstance(params.get('df'),(int,float)) and params['df'] > 2, 'Fixture Student-t returns require finite variance: df > 2.')
        elif family == 'deterministic':
            check(node['function_id'] in value['approved_function_registry'], 'Unaudited deterministic function.')
        else:
            raise ValueError(f'Family {family} is declared by schema but unsupported by this minimal semantic fixture validator; fail closed.')

def decision_check(value: dict[str, Any]) -> None:
    validate_schema('decision', value)
    check(value['selected_action'] in value['allowed_actions'], 'Selected action is not allowed.')
    check(value['estimated_cost_usd'] <= value['available_budget_usd'], 'Action exceeds available budget.')
    check(value['policy_approved'], 'Action lacks deterministic approval.')


def main() -> int:
    results: list[dict[str, Any]] = []
    def case(name: str, fn: Callable[[], None], reject: bool = False) -> None:
        error = None
        try:
            fn()
        except Exception as exc:
            error = f'{type(exc).__name__}: {exc}'
        passed = (error is not None) if reject else (error is None)
        results.append({'name':name,'expected':'reject' if reject else 'accept','passed':passed,'diagnostic':error})
    def changed(value: dict[str, Any], mutate: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
        v=copy.deepcopy(value); mutate(v); return v
    origin='2026-10-01T20:15:00Z'
    e=read_json(ROOT/'examples/evidence.synthetic.json')
    f=read_json(ROOT/'examples/forecast.synthetic.json')
    g=read_json(ROOT/'examples/graph.synthetic.json')
    d=read_json(ROOT/'examples/decision.synthetic.json')
    for name in ('evidence','forecast','graph','decision'):
        case(f'{name}: schema is well-formed',lambda name=name: Draft202012Validator.check_schema(read_json(ROOT/f'schemas/{name}.schema.json')))
    case('valid synthetic evidence',lambda:evidence_check(e,origin))
    case('valid marginal synthetic forecast',lambda:forecast_check(f))
    case('valid beta-Bernoulli synthetic graph',lambda:graph_check(g))
    case('valid zero-cost synthetic decision',lambda:decision_check(d))
    case('reject evidence after origin',lambda:evidence_check(read_json(ROOT/'examples/invalid/evidence_after_origin.json'),origin),True)
    case('reject over-budget dispatch',lambda:decision_check(read_json(ROOT/'examples/invalid/decision_over_budget.json')),True)
    case('certified historical import may occur later',lambda:evidence_check(changed(e,lambda x:x.update(availability_basis='certified_archive',ingested_at='2026-10-17T20:00:00Z')),origin))
    case('reject late received live observation',lambda:evidence_check(changed(e,lambda x:x.update(availability_basis='live_observed',ingested_at='2026-10-17T20:00:00Z')),origin),True)
    case('reject missing value presented as observed',lambda:evidence_check(changed(e,lambda x:x.update(value=None)),origin),True)
    case('reject missing status with numeric value',lambda:evidence_check(changed(e,lambda x:x.update(status='missing')),origin),True)
    case('reject nonfinite JSON',lambda:json.loads('{"x":NaN}',parse_constant=reject_constant),True)
    case('reject crossing quantiles',lambda:forecast_check(changed(f,lambda x:x['horizon_forecasts'][0]['variance_quantiles'][0].update(value=1))),True)
    case('reject wrong volatility unit conversion',lambda:forecast_check(changed(f,lambda x:x['horizon_forecasts'][0]['volatility_quantiles'][1].update(value=.99))),True)
    case('reject claimed joint paths without artifact',lambda:forecast_check(changed(f,lambda x:x['capabilities'].append('joint_paths'))),True)
    case('reject episode estimate on marginal-only output',lambda:forecast_check(changed(f,lambda x:x.update(episode_forecast={'method':'joint_paths','definition_id':'episode-v1','artifact_ref':'fictional-reference'}))),True)
    case('reject failed-model credit',lambda:forecast_check(changed(f,lambda x:x['failed_model_ids'].append('hand_authored_fixture_not_model'))),True)
    case('reject instantaneous cycle',lambda:graph_check(changed(g,lambda x:x['edges'].append({'source':'event_active','target':'event_probability','lag_sessions':0}))),True)
    case('lagged feedback passes structural cycle check only',lambda:graph_check(changed(g,lambda x:x['edges'].append({'source':'event_active','target':'event_probability','lag_sessions':1}))))
    case('reject negative beta shape',lambda:graph_check(changed(g,lambda x:x['nodes'][0]['distribution']['parameters'].update(alpha=-1))),True)
    case('reject bad beta support',lambda:graph_check(changed(g,lambda x:x['nodes'][0]['support'].update(upper=2))),True)
    case('reject unreferenced parameter',lambda:graph_check(changed(g,lambda x:x.update(edges=[]))),True)
    case('reject action outside allowed set',lambda:decision_check(changed(d,lambda x:x.update(selected_action='RUN_SPECIALIST'))),True)
    case('reject absent policy approval',lambda:decision_check(changed(d,lambda x:x.update(policy_approved=False))),True)
    def check_config() -> None:
        c=read_json(ROOT/'config/research.yaml')
        check(c['paid_budget']['max_per_run']==0 and c['paid_budget']['max_per_day']==0,'Default paid spending must be zero.')
        check(c['options']['execution_enabled'] is False,'Execution must be disabled.')
        check(c['learning']['automatic_production_promotion'] is False,'Automatic production promotion must be disabled.')
        for model in read_json(ROOT/'config/model_registry.json')['models']:
            check(not model['enabled'],'Unpinned candidate model enabled.')
    case('safe example defaults and disabled unpinned models',check_config)
    report={'scope':'Specification schemas and synthetic fixture invariants only. No application, real inference, backtest, posterior fit, calendar engine or profitability tests were run.',
      'status':'PASSED' if all(r['passed'] for r in results) else 'FAILED',
      'checked_at_utc':datetime.now(timezone.utc).isoformat(),'checks_total':len(results),'checks_passed':sum(r['passed'] for r in results),
      'planned_application_acceptance_requirements':78,'planned_application_acceptance_requirements_executed':0,'checks':results}
    (ROOT/'PACKAGE_VALIDATION.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(f"{report['status']}: {report['checks_passed']}/{report['checks_total']} package-only checks.")
    print('Application acceptance tests executed: 0. No forecasting or investment performance evaluated.')
    return 0 if report['status']=='PASSED' else 1

if __name__=='__main__':
    sys.exit(main())
