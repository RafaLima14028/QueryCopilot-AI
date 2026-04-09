from fastapi import APIRouter

router = APIRouter(
    prefix="/query",
    tags=["query"]
)


@router.post("/preview")
def generate_sql():
    pass


@router.post("/execute")
def execute_sql():
    pass


@router.post("/confirm")
def generate_sql():
    pass
