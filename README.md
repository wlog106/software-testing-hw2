# Software Testing HW2 – Calc with TDD

| Folder | Contents |
|---|---|
| `part1/` | Q1: Calc (add, subtract, multiply, divide) developed with TDD by hand, no AI |
| `part6/` | Q6: Calc extended with `modulo` and `power` via agentic TDD (Claude) |
| `.github/workflows/ci.yml` | Q2/Q3: CI running unittest, ruff and a 100% branch-coverage gate for every part |

Run the tests for one part:

```bash
cd part1   # or part6
python -m unittest -v CalcTest
```

To add another part (e.g. `part7/`), give it its own `Calc.py` and `CalcTest.py`
and add the folder name to both `part` matrices in `ci.yml`.
