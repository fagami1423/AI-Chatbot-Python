import imp
from typing import Optional
from question import question_routes
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/{question}}")
# def read_item(question: str):
#     return {"answer": question}

app.include_router(question_routes.router)