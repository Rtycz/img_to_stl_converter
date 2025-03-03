from fastapi import APIRouter
from fastapi.responses import JSONResponse
from processing.image_processing import process_image, apply_median_filter
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

@router.post("/api/v1/process/median-filter")
async def apply_median_filter_endpoint(data: dict):
    filename = data.get("filename")
    kernelSize = int(data.get("kernelSize", 3))

    photo_path = os.path.join("static/images", filename)
    processed_filename = apply_median_filter(photo_path, filename, kernelSize)

    return JSONResponse({"processed_filename": processed_filename})
