import imp
from typing import Optional
from question import question_routes
from product import product_routes
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/{question}}")
# def read_item(question: str):
#     return {"answer": question}

app.include_router(question_routes.router)
app.include_router(product_routes.router)