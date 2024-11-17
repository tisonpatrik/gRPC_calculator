from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    "/add/",
    status_code=status.HTTP_200_OK,
    name="Add",
)
def add_endpoint(query: int):
    return {"result": query + 2}
