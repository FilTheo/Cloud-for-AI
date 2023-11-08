import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import json
import uvicorn
import pandas as pd
from pickle import load


app = FastAPI()
with open("model.pkl", "rb") as f:
    model = load(f)


class user_input(BaseModel):
    satisfaction_level: float
    last_evaluation: float
    number_project: int
    average_montly_hours: int
    time_spend_company: int
    Work_accident: int
    promotion_last_5years: int
    departments: str
    salary: str


def predict(data):
    departments_list = [
        "IT",
        "RandD",
        "accounting",
        "hr",
        "management",
        "marketing",
        "product_mng",
        "sales",
        "support",
        "technical",
    ]
    data[-2] = departments_list.index(data[-2])
    salaries = ["low", "medium", "high"]
    data[-1] = salaries.index(data[-1])
    columns = [
        "satisfaction_level",
        "last_evaluation",
        "number_project",
        "average_montly_hours",
        "time_spend_company",
        "Work_accident",
        "promotion_last_5years",
        "departments",
        "salary",
    ]
    prediction = model.predict(pd.DataFrame([data], columns=columns))
    proba = model.predict_proba(pd.DataFrame([data], columns=columns))
    return prediction, proba


@app.get("/")
def welcome():
    return f"Welcome to app api"


@app.post("/predict")
def func(Input: user_input):
    data = [
        Input.satisfaction_level,
        Input.last_evaluation,
        Input.number_project,
        Input.average_montly_hours,
        Input.time_spend_company,
        Input.Work_accident,
        Input.promotion_last_5years,
        Input.departments,
        Input.salary,
    ]
    pred, proba = predict(data)
    output = {"prediction": int(pred[0]), "probability": float(proba[0][1])}
    return json.dumps(output)


if __name__ == "__main__":
    uvicorn.run("hello_world_fastapi:app")
