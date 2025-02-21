import os
from datetime import datetime, timedelta
import threading
import time

def cleanup_old_files():
    """Удаление файлов, которые старше установленного времени жизни."""
    now = datetime.now()
    for folder in ["static/images", "static/stl"]:
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
