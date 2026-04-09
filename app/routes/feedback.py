from fastapi import APIRouter

router = APIRouter(
    prefix="/feedback",
    tags=["feedback"]
)


@router.post("/")
def feedback():
    pass
