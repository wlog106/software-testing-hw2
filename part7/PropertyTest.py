"""Property-based / metamorphic tests for Part 7.

None of these tests hard-code an expected result. Each one draws random
inputs (fixed seed, so runs are reproducible) and checks a relation that
must hold between calls, e.g. subtract(add(a, b), b) == a.

Tests marked @unittest.expectedFailure document problems these properties
exposed; see the report for the discussion.
"""
import math
import random
import unittest

from Calc import Calculator

SAMPLES = 2000
SEED = 7


def small_ints(rng):
    # |a|, |b| < 2**26 keeps every product below 2**53, so floats stay exact
    return rng.randint(-(2**26), 2**26), rng.randint(-(2**26), 2**26)


def floats(rng):
    return rng.uniform(-1e6, 1e6), rng.uniform(-1e6, 1e6)


def big_ints(rng):
    # beyond 2**53 a float can no longer represent every integer
    return rng.randint(2**53, 2**60), rng.randint(2, 100)


def huge_floats(rng):
    return rng.uniform(1e300, 1e308), rng.uniform(1e10, 1e20)


def close(x, y):
    return math.isclose(x, y, rel_tol=1e-9, abs_tol=1e-6)


class TestCalculatorProperties(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        self.rng = random.Random(SEED)

    def check(self, gen, prop, nonzero_b=False):
        """Run prop on SAMPLES inputs; fail with the first counterexample."""
        for _ in range(SAMPLES):
            a, b = gen(self.rng)
            if nonzero_b and b == 0:
                continue
            self.assertTrue(prop(a, b), f"property failed for a={a!r}, b={b!r}")

    # --- algebraic laws -------------------------------------------------

    def test_add_and_multiply_are_commutative(self):
        c = self.calc
        for gen in (small_ints, floats):
            with self.subTest(inputs=gen.__name__):
                self.check(gen, lambda a, b: c.add(a, b) == c.add(b, a))
                self.check(gen, lambda a, b: c.multiply(a, b) == c.multiply(b, a))

    def test_identity_elements(self):
        c = self.calc
        for gen in (small_ints, floats):
            with self.subTest(inputs=gen.__name__):
                self.check(gen, lambda a, b: c.add(a, 0) == a)
                self.check(gen, lambda a, b: c.multiply(a, 1) == a)
                self.check(gen, lambda a, b: c.subtract(a, a) == 0)
                self.check(gen, lambda a, b: c.divide(a, 1) == a)

    # --- metamorphic round trips ----------------------------------------

    def test_subtract_undoes_add_ints(self):
        c = self.calc
        self.check(small_ints, lambda a, b: c.subtract(c.add(a, b), b) == a)

    def test_subtract_undoes_add_floats_within_tolerance(self):
        c = self.calc
        self.check(floats, lambda a, b: close(c.subtract(c.add(a, b), b), a))

    def test_divide_undoes_multiply_small_ints(self):
        c = self.calc
        self.check(small_ints, lambda a, b: c.divide(c.multiply(a, b), b) == a, nonzero_b=True)

    def test_divide_undoes_multiply_floats_within_tolerance(self):
        c = self.calc
        self.check(floats, lambda a, b: close(c.divide(c.multiply(a, b), b), a), nonzero_b=True)

    def test_divide_by_zero_always_raises(self):
        c = self.calc
        for _ in range(SAMPLES):
            a, _b = floats(self.rng)
            with self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
                c.divide(a, 0)

    # --- problems the properties exposed ----------------------------------

    @unittest.expectedFailure
    def test_subtract_undoes_add_floats_exactly(self):
        # Fails: floating-point rounding, e.g. (0.1 + 0.2) - 0.2 = 0.10000000000000003
        c = self.calc
        self.check(floats, lambda a, b: c.subtract(c.add(a, b), b) == a)

    @unittest.expectedFailure
    def test_divide_undoes_multiply_big_ints(self):
        # Fails: divide always returns a float, which cannot hold integers above 2**53,
        # e.g. divide(multiply(2**53 + 1, 3), 3) == 9007199254740992.0, not 2**53 + 1
        c = self.calc
        self.check(big_ints, lambda a, b: c.divide(c.multiply(a, b), b) == a)

    @unittest.expectedFailure
    def test_divide_undoes_multiply_huge_floats(self):
        # Fails: multiply overflows to inf without any error, so the round trip is lost
        c = self.calc
        self.check(huge_floats, lambda a, b: close(c.divide(c.multiply(a, b), b), a))


if __name__ == "__main__":
    unittest.main()
