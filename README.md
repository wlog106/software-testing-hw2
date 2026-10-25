# Software Testing HW2 – Calc with TDD

| Folder | Contents |
|---|---|
| `part1/` | Q1: Calc (add, subtract, multiply, divide) developed with TDD by hand, no AI |
| `part6/` | Q6: Calc extended with `modulo` and `power` via agentic TDD (Claude) |
| `part7/` | Q7: Calc written by a fresh agent from the Q1 tests only, plus property-based/metamorphic tests (`PropertyTest.py`) |
| `.github/workflows/ci.yml` | Q2/Q3: CI running unittest, ruff and a 100% branch-coverage gate for every part |

Run the tests for one part:

```bash
cd part1   # or part6, part7
python -m unittest discover -v -p "*Test.py"
```

To add another part, give it its own folder with `Calc.py` and one or more `*Test.py` files
and add the folder name to both `part` matrices in `ci.yml`.
