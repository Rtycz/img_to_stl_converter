from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from processing.image_processing import process_image
import os
from datetime import datetime
from typing import List

router = APIRouter()

@router.post("/api/v1/image")
async def upload_photo(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No photo part")

    filename = file.filename
    if filename == '':
        raise HTTPException(status_code=400, detail="No selected file")

    # Генерация префикса на основе текущей даты и времени
    prefix = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")[:-4]
    filename = f"{prefix}_{filename}"
    file_path = os.path.join("static/images", filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Обработка изображения с параметрами по умолчанию
    processed_filename = process_image(file_path, filename)

    return JSONResponse({
        "message": "Photo uploaded and processed successfully!",
        "filename": filename,
        "processed_filename": processed_filename
    })

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