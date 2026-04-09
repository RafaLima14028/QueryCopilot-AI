from fastapi import APIRouter

router = APIRouter(
    prefix="/history",
    tags=["history"]
)


@router.get("/")
def history():
    pass


@router.get("/{id}")
def history_by_id(id: int):
    pass
