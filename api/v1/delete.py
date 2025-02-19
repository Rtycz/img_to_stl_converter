from fastapi import APIRouter, Form, HTTPException
from typing import List
import os

router = APIRouter()

@router.delete("/api/v1/image")
async def delete_photos(filenames: List[str] = Form(...)):
    """input like ['13_02_2025_00_11_40_83_asd.png,13_02_2025_00_11_43_58_bsd.png']"""
    for filename in filenames[0].split(','):
        file_path = os.path.join("static/images", filename)
        processed_path = os.path.join("static/images", f"{filename.split('.')[0]}_processed.png")
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(processed_path):
            os.remove(processed_path)
    return "Photos deleted successfully!"
