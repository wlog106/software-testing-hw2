class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def modulo(self, a, b):
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("modulo only accepts integer operands")
        if b == 0:
            raise ValueError("Cannot modulo by zero")
        return a % b

    def power(self, a, b):
        if a == 0 and b < 0:
            raise ValueError("Cannot divide by zero")
        if a < 0 and b != int(b):
            raise ValueError("Negative base with a non-integer exponent gives a complex result")
        return a ** b
