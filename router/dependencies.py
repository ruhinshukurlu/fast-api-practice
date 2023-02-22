from fastapi import APIRouter, Depends
from fastapi.requests import Request

router = APIRouter(
    prefix='/dependencies',
    tags=['dependencies']
)


def convert_params(request: Request, seperator:str):
    queries = []
    for key,value in request.query_params.items():
        queries.append(f"{key} {seperator} {value}")
    return queries


def convert_headers(request:Request, seperator:str, queries = Depends(convert_params)):
    headers = []
    for key, value in request.headers.items():
        headers.append(f"{key} {seperator} {value}")
    return {
        "headers":headers,
        "queries":queries
    }


@router.get('')
def get_items(test:str, headers = Depends(convert_headers)):
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


class Account:
    def __init__(self, name:str, email:str):
        self.name = name
        self.email = email


@router.post('/user')
def create_account(name:str, email:str, password:str, account: Account = Depends(Account)):
    return {
        'name':account.name,
        "email": account.email
    }