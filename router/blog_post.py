from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

class Image(BaseModel):
    url:str
    alias:str

class BlogModel(BaseModel):
    title:str
    content:str
    published: Optional[bool]
    nb_comments:int
    tags: List[str] = []
    metadata: Dict[str, str] = {'key':'value'}
    # images: List[Image] # for the list of images
    image: Optional[Image] = None


@router.post('/new/{id}')
def create_blog(blog:BlogModel, id:int, version:int = 1):
    return {
            'id':id,
            'blog':blog,
            'version':version
        }


@router.post('/new/{id}/comment/{comment_id}')
def create_comment(
        blog:BlogModel,
        id:int,
        comment_title:str = Query(None,
            title='title of comment',
            description='Some description for the comment_title',
            alias='commentTitle',
            deprecated=True
        ),
        content: str = Body(
            ...,
            min_length=10,
            max_length=50,
            regex='^[a-z\s]*$'
        ),
        v: Optional[List[str]] = Query(None),
        comment_id: int = Path(None, gt=5, le=10)
    ):
    return {
        'blog':blog,
        'id':id,
        'comment_title':comment_title,
        'content':content,
        'versions':v,
        'comment_id':comment_id
    }

