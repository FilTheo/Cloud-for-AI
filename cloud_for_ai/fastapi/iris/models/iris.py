from pydantic import BaseModel, conlist
from typing import List


# Define the Iris model so FastAPI knows what to expect as data
class Iris(BaseModel):
    # ensure you get a list with 4 floats
    data: List[conlist(float, min_length=4, max_length=4)]
