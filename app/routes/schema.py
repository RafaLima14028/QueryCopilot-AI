from fastapi import APIRouter

router = APIRouter(
    prefix="/schema",
    tags=["schema"]
)


@router.get("/")
def schema():
    pass
