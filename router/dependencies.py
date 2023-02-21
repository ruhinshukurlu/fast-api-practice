from fastapi import APIRouter, Depends
from fastapi.requests import Request

router = APIRouter(
    prefix='/dependencies',
    tags=['dependencies']
)


def convert_headers(request:Request):
    headers = []
    for key, value in request.headers.items():
        headers.append(f"{key} -- {value}")
    return headers


@router.get('')
def get_items(headers = Depends(convert_headers)):
    return {
        "items":['a','b','c'],
        "headers":headers
    }


@router.post('/new')
def create_item(headers = Depends(convert_headers)):
    return {
        'info':"new item created",
        "headers":headers
    }