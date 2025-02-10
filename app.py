from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_AGE'] = timedelta(minutes=30)  # Установите время жизни файла

# Убедитесь, что папка для загрузок существует
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

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
        filename = f"{prefix}_{photo.filename}"
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)
        return jsonify({'message': 'Photo uploaded successfully!', 'filename': filename})

    return jsonify({'error': 'Upload failed'}), 500

@app.route('/delete', methods=['POST'])
def delete_photo():
    data = request.get_json()
    filename = data.get('filename')
    if filename:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return 'Photo deleted successfully!'
        else:
            return 'File not found!', 404
    return 'Bad request!', 400

def cleanup_old_files():
    """Удаление файлов, которые старше установленного времени жизни."""
    now = datetime.now()
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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
