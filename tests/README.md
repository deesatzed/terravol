# Test boundaries

`scaffold/` contains executable control/command tests. Run from the project root with Python 3.12:

```bash
PYTHONPATH=src python3.12 -B -m unittest discover -s tests/scaffold -v
```

Application tests do not exist yet. The 120 application requirements and planned test paths are in [the acceptance matrix](../docs/ACCEPTANCE_MATRIX.md). Create meaningful unit/property/integration/replay/adversarial tests at the responsible tickets. Never satisfy an application requirement with a scaffold test, skipped integration, mock provider or copied donor badge.

The archived v1 validator checks specification fixtures only. Reproduce it against temporary copies so its archived manifest and original receipt remain unchanged.
