import uvicorn
from fastapi import FastAPI, status, HTTPException
from typing import Dict
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel
import json

app = FastAPI()

class Product(BaseModel):
    product_id: int = 0
    name: str
    description: str | None = None
    price: float

store: Dict[int, Product] = {}

@app.post("/products")
async def create_product(product: Product):
    product.product_id = len(store) + 1
    store[product.product_id] = product
    return JSONResponse( 
        {"id": product.product_id},
          status_code=status.HTTP_201_CREATED,
    )

@app.get("/products/{product_id}")
async def read_product(product_id: int):
    if product_id not in store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Продукт с id {product_id} не найден",
        )
    product = jsonable_encoder(store[product_id])  
    return JSONResponse(
        product,
        status_code=status.HTTP_200_OK,)

@app.get("/products_download")
async def download_products():
    products = list(store.values())
    with open("products.json", "w") as f:
        json.dump(jsonable_encoder(products), f, indent=4, ensure_ascii=False)
    return FileResponse(
        "products.json",
        headers={
            "Content-Disposition": "attachment; filename=all_products.json",
        },
    )

@app.get('/', response_class = HTMLResponse)
def index():
    return "<b> Привет </b>" 
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)