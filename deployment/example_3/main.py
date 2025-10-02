from fastapi import FastAPI
from pydantic import BaseModel


def calculate(operation, x, y):
    """
    operation - takes the string ['add', 'subtract', 'multiply', 'divide']
    x - first number
    y - second number
    """
    if operation == "add":
        return x + y
    elif operation == "subtract":
        return x - y
    elif operation == "multiply":
        return x * y
    elif operation == "divide":
        return x / y
    else:
        return "Invalid operation"


class User_input(BaseModel):
    operation: str
    x: float
    y: float


app = FastAPI()


@app.post("/calculate")
def calculate_post(user_input: User_input):
    return calculate(user_input.operation, user_input.x, user_input.y)
