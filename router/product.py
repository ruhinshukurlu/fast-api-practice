from fastapi import APIRouter, Header
from typing import Optional, List
from fastapi.responses import Response, HTMLResponse, PlainTextResponse

router = APIRouter(
    prefix='/product',
    tags=['product']
)

products = ['phone', 'watch', 'camera']

@router.get('/all')
def get_all_products():
    data = " ".join(products)
    return Response(content=data, media_type='text/plain')


@router.get('/withheader')
def get_products(response:Response,  customer_header: Optional[List[str]] = Header(None)):
    response.headers['custom_response_header'] = ", ".join(customer_header)
    return products


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