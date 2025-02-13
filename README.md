# img_to_stl_converter

**Install requirements with:** pip install -r /path/to/requirements.txt <br>
**or** <br>
pip install fastapi uvicorn <br>
pip install opencv-python-headless <br>
pip install Jinja2 <br>
pip install python-multipart <br>
pip install numpy pillow numpy-stl <br>
pip install numpy pymesh


**run app with:** uvicorn main:app --reload

**clear venv** pip freeze | ForEach-Object { pip uninstall -y $_ }