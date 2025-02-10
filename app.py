from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return redirect(url_for('index'))

    photo = request.files['photo']

    if photo.filename == '':
        return redirect(url_for('index'))

    if photo:
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        photo.save(photo_path)
        return f'Photo uploaded successfully! <a href="{url_for("static", filename="uploads/" + photo.filename)}">View Photo</a>'

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)