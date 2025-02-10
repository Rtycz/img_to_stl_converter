from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_AGE'] = timedelta(minutes=15)  # Установите время жизни файла

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def cleanup_old_files():
    """Remove files older than MAX_AGE."""
    now = datetime.now()
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(file_path):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - file_time > app.config['MAX_AGE']:
                os.remove(file_path)
                print(f"Deleted {filename}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return 'No photo part'

    photo = request.files['photo']

    if photo.filename == '':
        return 'No selected file'

    if photo:
        # Generate a prefix based on the current date and time
        prefix = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")[:-4]
        filename = f"{prefix}_{photo.filename}"
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)
        return 'Photo uploaded successfully!'

    return 'Upload failed'

# Run the cleanup function periodically
def start_cleanup_thread():
    def run_cleanup():
        while True:
            cleanup_old_files()
            time.sleep(app.config['MAX_AGE'].total_seconds())

    thread = threading.Thread(target=run_cleanup)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    start_cleanup_thread()
    app.run(debug=True)
