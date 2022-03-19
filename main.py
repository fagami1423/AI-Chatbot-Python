import imp
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/{question}}")
def read_item(question: str):
    ## you guyz do the magic here
    return {"answer": question}