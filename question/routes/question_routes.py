import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from starlette import status

from database import mongodatabase
from ..schemas.schemas import serializeDict, serializeList
from bson import ObjectId
from ..models.question_model import Question
import train
import chat
import json

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/chatbot",
    tags=['Questions']
)

# print()

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get('/questions')
async def find_all_questions():
    return serializeList(mongodatabase.question.find())
 
@router.get('/train')
async def train_model():
    products = serializeList(mongodatabase.product.find())
    top_products = serializeList(mongodatabase.product.find({"is_top":1}))[:5]

    top_products_text = ",".join([product['name'] for product in top_products])
    questions_product = serializeList(mongodatabase.question.find({"tag":"products"}))
    questions_product[0]['responses']=["The top products right now are "+top_products_text,"The latest products right now are "+top_products_text]
    question_id = questions_product[0]['_id']
    # questions_product[0].pop("_id")
    del questions_product[0]["_id"]
    mongodatabase.question.find_one_and_update({"_id":ObjectId(question_id)},{
        "$set":dict(questions_product[0])
    })
    all_questions = serializeList(mongodatabase.question.find())
    for product in products:
        for question in all_questions:
            if product['category'].lower() == question['tag']:
                
                product_cat = serializeList(mongodatabase.product.find({"category":product['category']}))[:5]
                product_cat_text = ",".join([p['name'] for p in product_cat])
                id = question["_id"]
                question['responses']=["The main "+product['category']+"s available are "+product_cat_text]
                # del question["_id"]
                mongodatabase.question.find_one_and_update({"_id":ObjectId(id)},{
                    "$set": {"tag":question['tag'],"patterns":question["patterns"],"responses":question["responses"]}
                })
    intents = serializeList(mongodatabase.question.find())
    train.train(intents)
    return {"message": "Model has been trained and saved"}
 

@router.get('/{id}')
async def find_one_question(id):
    return serializeDict(mongodatabase.question.find_one({"_id":ObjectId(id)}))


@router.post('/')
async def create_question(**questions):

    # question_id = mongodatabase.question.insert_one(dict(question)).inserted_id
    # return serializeDict(mongodatabase.question.find_one({"_id":ObjectId(question_id)}))

    mongodatabase.question.drop()
    questions = json.loads(questions['questions'])
    mongodatabase.question.insert_many(questions)
    return "questions inserted successfully"
# @router.post('/')
# async def create_many_question(question: Question):
    
#     question_id = mongodatabase.question.insert_many(list(question)).inserted_id
#     return serializeDict(mongodatabase.question.find_one({"_id":ObjectId(question_id)}))


@router.put('/{id}')
async def update_question(id,question: Question):
    mongodatabase.question.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(question)
    })
    return serializeDict(mongodatabase.user.find_one({"_id":ObjectId(id)}))

@router.delete('/{id}')
async def delete_question(id,question: Question):
    
    return serializeDict(mongodatabase.user.find_one_and_delete({"_id":ObjectId(id)}))

@router.post("/chat")
async def post_input(input):
    userinputs = mongodatabase.userinput.find()
    # print(list(questions))
    userinputs = [userinput['question'] for userinput in userinputs]
    questions = serializeList(mongodatabase.question.find())
    response = chat.takeinput(input,questions)
    if input not in questions:
        question_id = mongodatabase.userinput.insert_one({"question":input}).inserted_id
    
    return response
