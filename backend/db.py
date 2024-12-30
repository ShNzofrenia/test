import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, Integer, String, REAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE = "my_database.db"

engine = create_engine(f"sqlite:///{DATABASE}")

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    cart_items = relationship("Cart", back_populates="user")

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_name = Column(String)
    quantity = Column(Integer)
    user = relationship("User", back_populates="cart_items")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    price = Column(REAL)


def open_db():
    db = SessionLocal()
    return db

def close_db(db):
    db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)


def add_user(db: SessionLocal, username, password):
    try:
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.add(user)
        db.commit()
        return True
    except:
        return False

def validate_user(db: SessionLocal, username, password):
    user = db.query(User).filter(User.username == username).first()
    if user and check_password_hash(user.password, password):
        return True
    return False

def add_to_cart(db: SessionLocal, username, item_name, quantity):
     user = db.query(User).filter(User.username == username).first()
     if not user:
          return False
     cart_item = Cart(user_id = user.id, item_name=item_name, quantity = quantity)
     db.add(cart_item)
     db.commit()
     return True
def get_cart(db: SessionLocal, username):
     user = db.query(User).filter(User.username == username).first()
     if not user:
          return None
     cart = db.query(Cart).filter(Cart.user_id == user.id).all()
     return cart
def delete_user(db: SessionLocal, username):
     user = db.query(User).filter(User.username == username).first()
     if not user:
          return False
     db.delete(user)
     db.commit()
     return True

def update_user_password(db: SessionLocal, username, new_password):
    try:
        hashed_password = generate_password_hash(new_password)
        user = db.query(User).filter(User.username == username).first()
        if not user:
              return False
        user.password = hashed_password
        db.commit()
        return True
    except:
         return False
def hash_password(password):
    return generate_password_hash(password)
def add_product(db: SessionLocal, name: str, price: float):
    try:
        product = Product(name = name, price = price)
        db.add(product)
        db.commit()
        return True
    except:
         return False
def remove_product(db: SessionLocal, name: str, price: float):
        product = db.query(Product).filter(Product.name == name, Product.price == price).first()
        if not product:
              return False
        db.delete(product)
        db.commit()
        return True
def get_products(db: SessionLocal):
     return db.query(Product).all()