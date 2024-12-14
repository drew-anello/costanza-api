from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/")
def read_root():
    return RedirectResponse(url="/getquotes/")
