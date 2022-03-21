import imp
from typing import Optional
from question import question_routes

from fastapi import FastAPI

app = FastAPI()

@app.get("/{question}}")
def read_item(question: str):
    return {"answer": question}

app.include_router(question_routes.router)