# calculator-service/models.py
from typing import Union


class Calculator:
    @staticmethod
    def calculate(a: float, b: float, operation: str) -> Union[float, str]:
        try:
            if operation == '+':
                return a + b
            elif operation == '-':
                return a - b
            elif operation == '*':
                return a * b
            elif operation == '/':
                return a / b if b != 0 else "Division by zero"
            else:
                return "Invalid operation"
        except Exception as e:
            return str(e)
