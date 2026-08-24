from fastapi import Depends, FastAPI
from models import Product
from database import session,engine
import database_models
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return ("hello Python") 

products = [
    Product(
        id=1,
        name="phone",
        description="budget phone",
        price=99,
        quantity=10,
    ),
    Product(
        id=2,
        name="laptop",
        description="gaming laptop",
        price=1200,
        quantity=5,
    ),
]

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()    

def init_db():
    db = session()
    try:
      for product in products:
        db.add(database_models.Product(**product.model_dump()))
        db.commit()
    finally:
        db.close()    

# init_db()

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id: int,db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product Not fount"
    # for product in products:
    #     if product.id == id:
    #         return product

@app.put("/products")
def get_all_products(id: int,product: Product, db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all().filter(database_models.Product.id == id).first()
    if db_products:
        db_products.name = product.name
        db_products.description = db_products.description
        db_products.price = product.price
        db_products.quantity = product.quantity
        db.commit()
        return "db_products updated"
    else: 
         return "No prodcuts found"
    
@app.post("/product")
def add_product(product: Product,id: int,db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    return product

@app.delete("/product")
def delet_product(id: int,product: Product, db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all().filter(database_models.Product.id == id).first()
    
    if db_products:
       db.delete(db_products)
       db.commit()
    else:
     return "Product not found"   