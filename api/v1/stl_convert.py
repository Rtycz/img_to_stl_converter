from fastapi import APIRouter
from fastapi.responses import JSONResponse
from processing.stl_conversation import convert_image_to_stl
import os

router = APIRouter()

@router.post("/api/v1/process/stl-convert")
async def convert_to_stl(data: dict):
    processed_filename = data.get("processed_filename")
    photo_path = os.path.join("static/images", processed_filename)
    stl_filename = convert_image_to_stl(photo_path, processed_filename)

    return JSONResponse({"stl_filename": stl_filename})
