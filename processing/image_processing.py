import cv2
import os

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
