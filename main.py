from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
import os
import cv2
from datetime import datetime, timedelta
import threading
import time

app = FastAPI()

# Убедитесь, что папка для загрузок существует
os.makedirs("static/images", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=templates.TemplateResponse)
async def read_index():
    return templates.TemplateResponse("index.html", {"request": {}})


@app.get("/adaptiveThreshold", response_class=templates.TemplateResponse)
async def read_adaptive_threshold():
    return templates.TemplateResponse("adaptiveThreshold.html", {"request": {}})


@app.post("/api/v1/image")
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


@app.delete("/api/v1/image")
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


@app.post("/api/v1/process/adaptive-threshold")
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


def process_image(photo_path, filename, maxValue=255, adaptiveMethod="ADAPTIVE_THRESH_GAUSSIAN_C", thresholdType="THRESH_BINARY", blockSize=11, C=2):
    # Чтение изображения
    image = cv2.imread(photo_path, cv2.IMREAD_GRAYSCALE)
    # Применение адаптивного порога
    adaptive_method = getattr(cv2, adaptiveMethod)
    threshold_type = getattr(cv2, thresholdType)
    processed_image = cv2.adaptiveThreshold(image, maxValue, adaptive_method, threshold_type, blockSize, C)
    # Сохранение обработанного изображения
    processed_filename = f"{filename.split('.')[0]}_processed.png"
    processed_path = os.path.join("static/images", processed_filename)
    cv2.imwrite(processed_path, processed_image)
    return processed_filename


def cleanup_old_files():
    """Удаление файлов, которые старше установленного времени жизни."""
    now = datetime.now()
    for folder in ["static/images"]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if now - file_time > timedelta(minutes=15):
                    os.remove(file_path)
                    print(f"Deleted {filename}")


def start_cleanup_thread():
    """Запуск фонового потока для периодической очистки старых файлов."""
    def run_cleanup():
        while True:
            cleanup_old_files()
            time.sleep(60)

    thread = threading.Thread(target=run_cleanup)
    thread.daemon = True
    thread.start()


@app.on_event("startup")
async def startup_event():
    start_cleanup_thread()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
