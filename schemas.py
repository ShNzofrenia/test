from pydantic import BaseModel
from typing import List
class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    token: str

class Message(BaseModel):
    message: str

class CartItem(BaseModel):
     item_name: str
     quantity: int
class CartResponse(BaseModel):
     cart : List[CartItem]

class ProductCreate(BaseModel):
      name: str
      price: float
class ProductResponse(BaseModel):
      name: str
      price: float
class ProductsResponse(BaseModel):
      products: List[ProductResponse]

class PasswordUpdate(BaseModel):
    new_password: str

class ItemCreate(BaseModel):
      item_name: str
      quantity: int

class Username(BaseModel):
     username : str
