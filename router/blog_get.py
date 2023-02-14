from fastapi import APIRouter
from typing import Optional
from enum import Enum

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


@router.get(
    '/all',
    summary="Retrieve all blogs",
    description='This api call simulates fetching all blogs',
    response_description="The list of available blogs"
)
def get_blogs(page = 1, page_size: Optional[int] = None):
  return {'message': f'All {page_size} blogs on page {page}'}


@router.get('/{id}/comments/{comment_id}', tags=['comment'])
def get_comment(id, comment_id, valid:bool = True, username:Optional[str] = None):
    return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}


class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@router.get('/type/{type}')
def get_blog_type(type:BlogType):
    return {'message': f'Blog type {type}'}