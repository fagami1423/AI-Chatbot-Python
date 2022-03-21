import datetime

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from starlette import status

from database import mongodatabase
from ..schemas.schemas import serializeDict, serializeList
from bson import ObjectId
from ..models.product_model import Question
import train

router = APIRouter(
    prefix="/product",
    tags=['Products']
)


@router.get('/')
async def find_all_products():
    return serializeList(mongodatabase.product.find())
 
@router.get('/train')
async def train_model():
    intents = serializeList(mongodatabase.product.find())
    print(intents)
    # train.train(intents)
    ## todo: call a function which will fetch all the questions and train a model and save it.
    return {"message": "Model has been trained and saved"}
 

@router.get('/{id}')
async def find_one_product(id):
    return serializeDict(mongodatabase.product.find_one({"_id":ObjectId(id)}))


@router.post('/')
async def create_product(product: Question):
    product_id = mongodatabase.product.insert_one(dict(product)).inserted_id
    return serializeDict(mongodatabase.product.find_one({"_id":ObjectId(product_id)}))


@router.put('/{id}')
async def update_product(id,product: Question):
    mongodatabase.product.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(product)
    })
    return serializeDict(mongodatabase.user.find_one({"_id":ObjectId(id)}))


# @router.delete('/{id}')
# async def delete_user(id,user: User, Authorize:AuthJWT=Depends()):
#     try:
#         Authorize.jwt_required()
#
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid Token"
#         )
#     return serializeDict(mongodatabase.user.find_one_and_delete({"_id":ObjectId(id)}))