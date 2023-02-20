from fastapi import APIRouter, Header, Cookie, Form
from typing import Optional, List
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
import time


router = APIRouter(
    prefix='/product',
    tags=['product']
)

products = ['phone', 'watch', 'camera']


async def time_consuming_functionality():
    time.sleep(5)
    return "ok"


@router.post('/new')
def create_product(name:str = Form(...)):
    products.append(name)
    return products

@router.get('/all')
async def get_all_products():
    await time_consuming_functionality()
    data = " ".join(products)
    response = Response(content=data, media_type='text/plain')
    response.set_cookie(key='test_cookie', value='test_cookie_value')
    return response


@router.get('/withheader')
def get_products(
    response:Response,
    customer_header: Optional[List[str]] = Header(None),
    test_cookie : Optional[str] = Cookie(None)
    ):
    if customer_header:
        response.headers['custom_response_header'] = ", ".join(customer_header)
    return {
        "data":products,
        "custom_headers":customer_header,
        "cookie":test_cookie
    }


@router.get('/{id}', responses={
    200 : {
        "content":{
            "text/html":{
                "example":"<div>Product</div>"
            }
        },
        "description":"Returns the HTML for an object"
    },
    404:{
        "content":{
            "text/plain":{
                "example":"Product not available"
            }
        },
        "description":"A cleartext error message"
    }
})
def get_product(id:int):
    if id >= len(products):
        out = "Product not found"
        return PlainTextResponse(status_code=404, content=out, media_type='text/plain')
    else:
        product = products[id]
        out = f"""
            <head>
                <style>
                    .product{{
                        width:500px;
                        height:30px;
                        background-color:blue;
                    }}
                </style>
            </head>
            <div class = "product">{product}</div>
        """
        return HTMLResponse(content=out, media_type='text/html')