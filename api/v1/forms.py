from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from processing.image_processing import process_image
import os
from datetime import datetime
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=templates.TemplateResponse)
async def read_index():
    return templates.TemplateResponse("index.html", {"request": {}})

@router.get("/adaptiveThreshold", response_class=templates.TemplateResponse)
async def read_adaptive_threshold():
    return templates.TemplateResponse("adaptiveThreshold.html", {"request": {}})