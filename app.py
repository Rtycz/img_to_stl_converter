from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os
from datetime import datetime, timedelta
import threading
import time
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed'
app.config['MAX_AGE'] = timedelta(minutes=30)  # Установите время жизни файла

# Убедитесь, что папки для загрузок и обработанных файлов существуют
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo part'}), 400

    photo = request.files['photo']

    if photo.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if photo:
        # Генерация префикса на основе текущей даты и времени
        prefix = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")[:-4]
        filename = f"{prefix}_{secure_filename(photo.filename)}"
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)

        # Обработка изображения с параметрами по умолчанию
        processed_filename = process_image(photo_path, filename)

        return jsonify({'message': 'Photo uploaded and processed successfully!', 'filename': filename, 'processed_filename': processed_filename})

    return jsonify({'error': 'Upload failed'}), 500

@app.route('/process-image', methods=['POST'])
def process_image_with_params():
    data = request.get_json()
    filename = data.get('filename')
    maxValue = int(data.get('maxValue', 255))
    adaptiveMethod = data.get('adaptiveMethod', 'ADAPTIVE_THRESH_GAUSSIAN_C')
    thresholdType = data.get('thresholdType', 'THRESH_BINARY')
    blockSize = int(data.get('blockSize', 11))
    C = int(data.get('C', 2))

    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    processed_filename = process_image(photo_path, filename, maxValue, adaptiveMethod, thresholdType, blockSize, C)

    return jsonify({'processed_filename': processed_filename})

def process_image(photo_path, filename, maxValue=255, adaptiveMethod='ADAPTIVE_THRESH_GAUSSIAN_C', thresholdType='THRESH_BINARY', blockSize=11, C=2):
    # Чтение изображения
    image = cv2.imread(photo_path, cv2.IMREAD_GRAYSCALE)
    # Применение адаптивного порога
    adaptive_method = getattr(cv2, adaptiveMethod)
    threshold_type = getattr(cv2, thresholdType)
    processed_image = cv2.adaptiveThreshold(image, maxValue, adaptive_method, threshold_type, blockSize, C)
    # Сохранение обработанного изображения
    processed_filename = f"processed_{filename}"
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
    cv2.imwrite(processed_path, processed_image)
    return processed_filename

@app.route('/delete', methods=['POST'])
def delete_photos():
    data = request.get_json()
    filenames = data.get('filenames', [])
    for filename in filenames:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], f"processed_{filename}")
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(processed_path):
            os.remove(processed_path)
    return 'Photos deleted successfully!'

def cleanup_old_files():
    """Удаление файлов, которые старше установленного времени жизни."""
    now = datetime.now()
    for folder in [app.config['UPLOAD_FOLDER'], app.config['PROCESSED_FOLDER']]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if now - file_time > app.config['MAX_AGE']:
                    os.remove(file_path)
                    print(f"Deleted {filename}")

def start_cleanup_thread():
    """Запуск фонового потока для периодической очистки старых файлов."""
    def run_cleanup():
        while True:
            cleanup_old_files()
            time.sleep(app.config['MAX_AGE'].total_seconds())

    thread = threading.Thread(target=run_cleanup)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    start_cleanup_thread()  # Запуск фонового потока для очистки
    app.run(host='0.0.0.0', port=5000, debug=True)
