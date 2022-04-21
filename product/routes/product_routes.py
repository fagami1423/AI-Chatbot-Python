import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from starlette import status

from database import mongodatabase
from ..schemas.schemas import serializeDict, serializeList
from bson import ObjectId
from ..models.product_model import Product
import train
import chat
import json

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/product",
    tags=['Products']
)

# print()

# @router.get("/", response_class=HTMLResponse)
# def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

@router.get('/products')
async def find_all_products():
    return serializeList(mongodatabase.product.find())
 

@router.get('/{id}')
async def find_one_product(id):
    return serializeDict(mongodatabase.product.find_one({"_id":ObjectId(id)}))

@router.post('/')
async def create_many_product(**product):
    mongodatabase.product.drop()
    products = json.loads(product['product'])
    mongodatabase.product.insert_many(products)
    return "Products inserted successfully"

@router.put('/{id}')
async def update_product(id,product: Product):
    mongodatabase.product.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(product)
    })
    return serializeDict(mongodatabase.user.find_one({"_id":ObjectId(id)}))

@router.delete('/{id}')
async def delete_product(id,product: Product):
    return serializeDict(mongodatabase.user.find_one_and_delete({"_id":ObjectId(id)}))


