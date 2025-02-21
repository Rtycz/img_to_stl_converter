from PIL import Image
import numpy as np
from stl import mesh
import stl

def convert_image_to_stl(image_path, processed_filename, scale_factor=0.5):
    print(image_path, scale_factor)
    # Загрузка изображения и уменьшение его размера
    image = Image.open(image_path)
    width, height = image.size
    new_size = (int(width * scale_factor), int(height * scale_factor))
    image = image.resize(new_size, Image.NEAREST)
    image_array = np.array(image)

    # Определение размеров изображения
    height, width = image_array.shape

    # Создание сетки для 3D модели
    vertices = []
    for i in range(height):
        for j in range(width):
            z = 10 if image_array[i, j] > 127 else 0  # Высота 10 мм для светлых пикселей, 0 мм для темных
            vertices.append([j, i, z])

    # Создание треугольников для STL файла
    faces = []
    for i in range(height - 1):
        for j in range(width - 1):
            v1 = i * width + j
            v2 = v1 + 1
            v3 = v1 + width
            v4 = v3 + 1
            faces.append([v1, v2, v3])
            faces.append([v2, v4, v3])

    # Создание STL меша
    stl_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            stl_mesh.vectors[i][j] = vertices[face[j]]

    # Сохранение STL файла в бинарном формате
    output_filename = image_path.replace('.', '_processed.') + '.stl'
    stl_mesh.save(output_filename, mode=stl.Mode.BINARY)

    return output_filename
