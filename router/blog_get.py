from fastapi import APIRouter
from typing import Optional

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