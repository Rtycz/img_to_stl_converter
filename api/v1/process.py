from fastapi import APIRouter
from fastapi.responses import JSONResponse
from processing.image_processing import process_image
import os

router = APIRouter()

@router.post("/api/v1/process/adaptive-threshold")
async def process_image_with_params(data: dict):
    filename = data.get("filename")
    maxValue = int(data.get("maxValue", 255))
    adaptiveMethod = data.get("adaptiveMethod", "ADAPTIVE_THRESH_GAUSSIAN_C")
    thresholdType = data.get("thresholdType", "THRESH_BINARY")
    blockSize = int(data.get("blockSize", 11))
    C = int(data.get("C", 2))

    photo_path = os.path.join("static/images", filename)
    processed_filename = process_image(photo_path, filename, maxValue, adaptiveMethod, thresholdType, blockSize, C)

    return JSONResponse({"processed_filename": processed_filename})
