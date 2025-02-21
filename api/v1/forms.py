from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_index():
    return templates.TemplateResponse("index.html", {"request": {}})


@router.get("/adaptiveThreshold", response_class=HTMLResponse)
async def read_adaptive_threshold():
    return templates.TemplateResponse("adaptiveThreshold.html", {"request": {}})
