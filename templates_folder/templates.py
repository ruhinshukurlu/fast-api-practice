from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from schemas import ProductBase

router = APIRouter(
    prefix='/templates',
    tags=['templates']
)


tempaltes = Jinja2Templates(directory="templates_folder")


@router.post('/products/{id}', response_class=HTMLResponse)
def get_product(id:str, product:ProductBase, request:Request):
    return tempaltes.TemplateResponse(
        "product.html",
        {
            "request":request,
            "id":id,
            "title":product.title,
            "description":product.description,
            "price":product.price
        }
    )