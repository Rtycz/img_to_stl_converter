from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from processing.image_processing import process_image
import os
from datetime import datetime

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
