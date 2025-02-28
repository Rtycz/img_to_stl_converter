from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from api.v1 import image, process, stl_convert, forms
from processing.file_cleanup import start_cleanup_thread
from contextlib import asynccontextmanager

app = FastAPI()

# Убедитесь, что папка для загрузок существует
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/stl", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(image.router)
app.include_router(process.router)
app.include_router(stl_convert.router)
app.include_router(forms.router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, который выполняется при старте приложения
    start_cleanup_thread()
    yield
    # Код, который выполняется при завершении работы приложения

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
