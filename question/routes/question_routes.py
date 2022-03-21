import datetime

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from starlette import status

from database import mongodatabase
from ..schemas.schemas import serializeDict, serializeList
from bson import ObjectId
from ..models.question_model import Question
import train

router = APIRouter(
    prefix="/question",
    tags=['Questions']
)


@router.get('/')
async def find_all_questions():
    return serializeList(mongodatabase.question.find())
 
@router.get('/train')
async def train_model():
    intents = serializeList(mongodatabase.question.find())
    print(intents)
    ## train.train(intents)
    return {"message": "Model has been trained and saved"}
 

@router.get('/{id}')
async def find_one_question(id):
    return serializeDict(mongodatabase.question.find_one({"_id":ObjectId(id)}))


@router.post('/')
async def create_question(question: Question):
    question_id = mongodatabase.question.insert_one(dict(question)).inserted_id
    return serializeDict(mongodatabase.question.find_one({"_id":ObjectId(question_id)}))


@router.put('/{id}')
async def update_question(id,question: Question):
    mongodatabase.question.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(question)
    })
    return serializeDict(mongodatabase.user.find_one({"_id":ObjectId(id)}))

@router.delete('/{id}')
async def delete_question(id,question: Question):
    
    return serializeDict(mongodatabase.user.find_one_and_delete({"_id":ObjectId(id)}))