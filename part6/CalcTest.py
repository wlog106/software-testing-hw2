import unittest
from Calc import Calculator

class TestCalculator(unittest.TestCase):
    def test_add(self):
        calc = Calculator()
        for x, y, expected in [
            (2, 3, 5),
            (79, -1, 78)
        ]:
            with self.subTest(x=x, y=y):
                result = calc.add(x, y)
                self.assertIsInstance(result, int, "int + int = int")
                self.assertEqual(result, expected)

        for x, y, expected in [
            (1.0, 2, 3.0),
            (7, -6.0, 1.0),
            (1.5, 2.4, 3.9),
            (4.0, 2.0, 6.0),
            (4.7, -4.8, -0.1)
        ]:
            with self.subTest(x=x, y=y):
                result = calc.add(x, y)
                self.assertIsInstance(result, float, "if any of the operand is float, result = float")
                self.assertAlmostEqual(result, expected)

    def test_subtract(self):
        calc = Calculator()
        for x, y, expected in [
            (3, 2, 1),
            (1000, 567, 433),
            (13, -8, 21)
        ]:
            with self.subTest(x=x, y=y):
                result = calc.subtract(x, y)
                self.assertIsInstance(result, int, "int - int = int")
                self.assertEqual(result, expected)

        for x, y, expected in [
            (3.0, 2, 1.0),
            (-1, -0.7, -0.3),
            (3.9, 1.5, 2.4),
            (2.0999, -0.0001, 2.1)
        ]:
            with self.subTest(x=x, y=y):
                result = calc.subtract(x, y)
                self.assertIsInstance(result, float, "if any of the operand is float, result = float")
                self.assertAlmostEqual(result, expected)

    def test_multiply(self):
        calc = Calculator()
        for x, y, expected in [
            (3, 2, 6),
            (1000, 567, 567000),
            (-1, -1, 1)
        ]:
            with self.subTest(x=x, y=y):
                result = calc.multiply(x, y)
                self.assertIsInstance(result, int, "int * int = int")
                self.assertEqual(result, expected)

        for x, y, expected in [
            (3.0, 2, 6.0),
            (2, -4.0, -8.0),
            (3.9, 1.5, 5.85),
            (2.0999, -0.1, -0.20999)
        ]:
            with self.subTest(x=x, y=y):
                result = calc.multiply(x, y)
                self.assertIsInstance(result, float, "if any of the operand is float, result = float")
                self.assertAlmostEqual(result, expected)

    def test_divide(self):
        calc = Calculator()
        for x, y, expected in [
            (9, 3, 3.0),
            (3.0, -2, -1.5),
            (3.9, 1.5, 2.6),
            (-2.0999, -0.1, 20.999),
        ]:
            with self.subTest(x=x, y=y):
                result = calc.divide(x, y)
                self.assertIsInstance(result, float, "division should always return float")
                self.assertAlmostEqual(result, expected)

        for x, y in [
            (5, 0),
            (4, 0.0)
        ]:
            with self.subTest(x=x, y=y), self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
                    calc.divide(x, y)

    def test_modulo(self):
        calc = Calculator()
        # Decision: Python-style modulo, the result takes the sign of the divisor
        for x, y, expected in [
            (7, 3, 1),
            (6, 3, 0),
            (-7, 3, 2),
            (7, -3, -2),
            (-7, -3, -1),
        ]:
            with self.subTest(x=x, y=y):
                result = calc.modulo(x, y)
                self.assertIsInstance(result, int, "int % int = int")
                self.assertEqual(result, expected)

        # Decision: modulo only accepts integers; any non-int operand raises TypeError
        for x, y in [
            (7.5, 2),
            (7, 2.0),
            (-7.5, -2.5),
        ]:
            with self.subTest(x=x, y=y), self.assertRaisesRegex(TypeError, "integer"):
                calc.modulo(x, y)

    def test_modulo_by_zero(self):
        calc = Calculator()
        # Decision: modulo by zero raises ValueError, consistent with divide
        for x in [5, 0, -5]:
            with self.subTest(x=x), self.assertRaisesRegex(ValueError, "Cannot modulo by zero"):
                calc.modulo(x, 0)

    def test_power(self):
        calc = Calculator()
        # Decision: int ** non-negative int = int, and power(0, 0) = 1
        for x, y, expected in [
            (2, 3, 8),
            (-2, 3, -8),
            (-2, 2, 4),
            (5, 0, 1),
            (0, 0, 1),
        ]:
            with self.subTest(x=x, y=y):
                result = calc.power(x, y)
                self.assertIsInstance(result, int, "int ** non-negative int = int")
                self.assertEqual(result, expected)

        # Decision: a negative exponent returns a float
        for x, y, expected in [
            (2, -1, 0.5),
            (4, -2, 0.0625),
            (-2, -1, -0.5),
        ]:
            with self.subTest(x=x, y=y):
                result = calc.power(x, y)
                self.assertIsInstance(result, float, "negative exponent returns float")
                self.assertAlmostEqual(result, expected)

        # Decision: floats are allowed (float ** float, float ** int, int ** float)
        # as long as the result is real; the result is a float
        for x, y, expected in [
            (2.5, 2, 6.25),
            (-1.5, 2, 2.25),
            (4, 0.5, 2.0),
            (2.0, 3.0, 8.0),
            (-2, 2.0, 4.0),
            (8.0, -1 / 3, 0.5),
        ]:
            with self.subTest(x=x, y=y):
                result = calc.power(x, y)
                self.assertIsInstance(result, float, "float operand returns float")
                self.assertAlmostEqual(result, expected)

        # Decision: zero to a negative power raises ValueError, like divide
        for x, y in [
            (0, -1),
            (0, -2),
            (0.0, -1),
        ]:
            with self.subTest(x=x, y=y), self.assertRaisesRegex(ValueError, "Cannot divide by zero"):
                calc.power(x, y)

        # Decision: a negative base with a fractional exponent would give a complex
        # number, so it raises ValueError
        for x, y in [
            (-8, 0.5),
            (-8, -0.5),
            (-2.5, 0.5),
            (-8, 1.5),
        ]:
            with self.subTest(x=x, y=y), self.assertRaisesRegex(ValueError, "complex"):
                calc.power(x, y)

if __name__ == "__main__":
    unittest.main()
