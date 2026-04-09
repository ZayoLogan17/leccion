from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, SQLModel
from models import Product
from database import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/products")
def create_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product

@app.get("/products")
def get_products():
    with Session(engine) as session:
        return session.exec(select(Product)).all()

@app.get("/products/{id}")
def get_product(id: int):
    with Session(engine) as session:
        product = session.get(Product, id)
        if not product:
            raise HTTPException(status_code=404, detail="No encontrado")
        return product

@app.put("/products/{id}")
def update_product(id: int, new_data: Product):
    with Session(engine) as session:
        product = session.get(Product, id)
        if not product:
            raise HTTPException(status_code=404, detail="No encontrado")

        product.name = new_data.name
        product.description = new_data.description
        product.price = new_data.price
        product.stock = new_data.stock
        product.image_url = new_data.image_url

        session.add(product)
        session.commit()
        session.refresh(product)
        return product

@app.delete("/products/{id}")
def delete_product(id: int):
    with Session(engine) as session:
        product = session.get(Product, id)
        if not product:
            raise HTTPException(status_code=404, detail="No encontrado")

        session.delete(product)
        session.commit()
        return {"mensaje": "Eliminado"}