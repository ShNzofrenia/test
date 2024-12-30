from fastapi import FastAPI, Depends, HTTPException, Header
from typing import List
from backend.db import open_db, close_db, create_tables, add_user, validate_user, add_to_cart, get_cart, delete_user, update_user_password, add_product, remove_product, get_products, SessionLocal, Product, Cart
from backend.regex import is_valid_login, is_valid_password
from backend.token import create_jwt, validate_jwt, SECRET_KEY
from schemas import UserCreate, Token, Message, CartResponse, ProductCreate, ProductsResponse, PasswordUpdate, ItemCreate, Username
import os
from sqlalchemy.orm import Session

app = FastAPI()


def get_db():
    db = open_db()
    try:
        yield db
    finally:
        close_db(db)
async def get_current_user(authorization: str = Header(None), db: SessionLocal = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ", 1)[1]
    username = validate_jwt(token)
    if not username:
         raise HTTPException(status_code=401, detail="Invalid token")
    return username

@app.post('/login', response_model=Token)
def login(user_data: UserCreate, db: SessionLocal = Depends(get_db)):
    if not is_valid_login(user_data.username) or not is_valid_password(user_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if validate_user(db, user_data.username, user_data.password):
        token = create_jwt(user_data.username)
        return Token(token=token)
    else:
         raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get('/validate-token', response_model=Message)
async def validate_token(username: str = Depends(get_current_user)):
    return Message(message=f"Token is valid for user: {username}")

@app.post('/add-to-cart', response_model=Message)
async def add_to_cart_route(item: ItemCreate, username: str = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if not add_to_cart(db, username, item.item_name, item.quantity):
           raise HTTPException(status_code=400, detail="Failed to add item")
    return Message(message="Item added to cart")

@app.delete('/delete-user', response_model=Message)
async def delete_user_route(username: str = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if not delete_user(db, username):
        raise HTTPException(status_code=400, detail="User deletion failed")
    return Message(message="User deleted successfully")
@app.put('/update-password', response_model=Message)
async def update_password_route(password_data: PasswordUpdate, username: str = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if not update_user_password(db, username, password_data.new_password):
           raise HTTPException(status_code=400, detail="Password update failed")
    return Message(message="Password updated successfully")

@app.post('/add-user', response_model=Message)
def add_user_route(user_data: UserCreate, db: SessionLocal = Depends(get_db)):
    if not is_valid_login(user_data.username) or not is_valid_password(user_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if not add_user(db, user_data.username, user_data.password):
          raise HTTPException(status_code=400, detail="User creation failed")
    return Message(message="User created successfully")

@app.post('/add-product', response_model=Message)
async def add_product_route(product_data: ProductCreate, username: str = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
     if not add_product(db, product_data.name, product_data.price):
           raise HTTPException(status_code=400, detail="Product creation failed")
     return Message(message = "Product added successfully")
@app.post('/remove-from-product', response_model=Message)
async def remove_product_route(product_data: ProductCreate, username: str = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if not remove_product(db, product_data.name, product_data.price):
        raise HTTPException(status_code=400, detail = "Product removal failed")
    return Message(message="Product removed successfully")

@app.post('/get-cart', response_model = CartResponse)
async def get_cart_route(username: Username , db: SessionLocal = Depends(get_db), user: str = Depends(get_current_user)):
     cart = get_cart(db, username.username)
     if not cart:
            raise HTTPException(status_code=400, detail = "Cart is empty")
     return CartResponse(cart=[{"item_name": item.item_name, "quantity": item.quantity} for item in cart])


@app.get('/get-products', response_model=ProductsResponse)
async def get_products_route(username: str = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
        products = get_products(db)
        if not products:
             raise HTTPException(status_code=400, detail = "Products list is empty")
        return ProductsResponse(products=[{"name": product.name, "price": product.price} for product in products])
@app.get('/db-info', response_model=dict)
async def get_db_info(db: SessionLocal = Depends(get_db)):
       tables = Base.metadata.tables
       table_info = {}
       for table_name, table in tables.items():
          columns = [{"name": column.name, "type": str(column.type)} for column in table.columns]
          table_info[table_name] = columns
       return table_info