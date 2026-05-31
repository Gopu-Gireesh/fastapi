from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session,engine
import database_models
from sqlalchemy.orm import Session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)
database_models.Base.metadata.create_all(bind=engine)


@app.get('/')
def greet():
    return products

products = [
    Product(id=1, name="Laptop", description="High-performance laptop", price=999.99, quantity=10),
    Product(id=2, name="Mouse", description="Wireless mouse", price=29.99, quantity=50),
    Product(id=3, name="Keyboard", description="Mechanical keyboard", price=79.99, quantity=  30)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Product).count
    if count ==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
    db.commit()



@app.get('/products')
def get_all_products(db: Session= Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products


@app.get('/products/{id}')
def get_product_by_id(id:int,db: Session= Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return {"error": "Product not found"}

@app.post('/products') 
def add_product(product:Product,db: Session= Depends(get_db)):
    db.add(database_models.Product(**product.model_dump())) 
    db.commit()
    return product

@app.put('/products/{id}')
def update_product(id:int, updated_product:Product,db: Session= Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.description = updated_product.description
        db_product.price = updated_product.price
        db_product.quantity = updated_product.quantity
        db.commit()
        return "Product updated successfully"
    else:
        return {"error": "Product not found"}

@app.delete('/products/{id}')
def delete_product(id:int,db: Session= Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted"}
    return {"error": "Product not found"}