from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

fake_token = "this_is_secret"

fake_db = [
    {
        "id": 1,
        "title": "Monitor",
        "price": 200,
        "qty": 10
    },
    {
        "id": 2,
        "title": "Mouse",
        "price": 12,
        "qty": 10
    },
    {
        "id": 3,
        "title": "Keyboard",
        "price": 25,
        "qty": 10
    }
]


class Product(BaseModel):
    id: int
    title: str
    price: int
    qty: int


class CreateProduct(BaseModel):
    title: str
    price: int
    qty: int


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.get("/products/", response_model=List[Product])
async def get_products(x_token: str = Header()):
    if x_token != fake_token:
        raise HTTPException(status_code=400, detail="invalid token")

    products = fake_db

    return products


@app.get("/products/{id}", response_model=Product)
async def get_product_by_id(id: int, x_token: str = Header()):
    if x_token != fake_token:
        raise HTTPException(status_code=400, detail="invalid token")

    products = fake_db
    for product in products:
        if product["id"] == id:
            return product

    raise HTTPException(status_code=404, detail="product not found")


@app.post("/products/", response_model=Product)
async def create_product(product: CreateProduct, x_token: str = Header()):
    if x_token != fake_token:
        raise HTTPException(status_code=400, detail="invalid token")

    products = fake_db

    new_product = product.dict()
    new_product["id"] = len(products) + 1

    products.append(new_product)

    return new_product


def reformat_product_name(name=""):
    if name:
        name_splited = name.split()
        new_name = "{}-{}".format(name_splited[0].upper(), len(fake_db))

        return new_name

    return "default-name"
