from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from calculator.src.validations.requests import AddRequest

router = APIRouter()


@router.get(
    "/add/",
    status_code=status.HTTP_200_OK,
    name="Add",
)
def add_endpoint(
    query: AddRequest = Depends(),
):
    try:
        result = query.x + query.y
        return result
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.errors(),
        )
