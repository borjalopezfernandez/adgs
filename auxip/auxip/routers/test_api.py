from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def read_root():
    return {"not": "supported"}


@router.get("/test")
async def test_db():
    return {"test": "database"}
