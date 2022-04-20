from urllib import response
from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    name: str
    category: str
    company: str
    manu_date: Optional [str]
    expiry_date: Optional [str]
    


