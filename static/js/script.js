// static/js/script.js

let uploadedFilenames = []; // Список для хранения имен загруженных файлов

document.getElementById('photoInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        const preview = document.getElementById('preview');
        const loader = document.getElementById('loader');
        const previewImage = document.getElementById('previewImage');
        const processedImageContainer = document.getElementById('processedImageContainer');
        const processedImage = document.getElementById('processedImage');

        // Показать индикатор загрузки
        loader.style.display = 'block';
        preview.style.display = 'block';
        previewImage.style.display = 'none';
        processedImageContainer.style.display = 'none';

        reader.onload = function(e) {
            // Отображение превью изображения после загрузки
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
            loader.style.display = 'none';
        };
        reader.readAsDataURL(file);

        // Создание объекта FormData и добавление файла
        const formData = new FormData();
        formData.append('file', file);

        // Отправка файла на сервер с использованием fetch
        fetch('/api/v1/image', {
            method: 'POST',
            body: formData
        }).then(response => response.json())
          .then(data => {
              uploadedFilenames.push(data.filename); // Добавление имени файла в список
              // Отображение обработанного изображения
              updateProcessedImage(data.filename);
          }).catch(error => {
              console.error('Ошибка при загрузке фото:', error);
          });
    }
});

// Обработчик события beforeunload для удаления всех файлов при закрытии вкладки
window.addEventListener('beforeunload', function(event) {
    if (uploadedFilenames.length > 0) {
        // Уведомление сервера об удалении всех файлов
        fetch('/api/v1/image', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ filenames: uploadedFilenames })
        }).then(response => response.text())
          .then(data => {
              console.log(data);
          }).catch(error => {
              console.error('Ошибка при удалении фото:', error);
          });
    }
});

// Функция для обновления обработанного изображения
function updateProcessedImage(filename) {
    const maxValue = document.getElementById('maxValue').value;
    const adaptiveMethod = document.getElementById('adaptiveMethod').value;
    const thresholdType = document.getElementById('thresholdType').value;
    const blockSize = document.getElementById('blockSize').value;
    const C = document.getElementById('C').value;

    fetch('/api/v1/process/adaptive-threshold', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            filename,
            maxValue,
            adaptiveMethod,
            thresholdType,
            blockSize,
            C
        })
    }).then(response => response.json())
      .then(data => {
          const processedImage = document.getElementById('processedImage');
          const processedImageContainer = document.getElementById('processedImageContainer');
          processedImage.src = `/static/images/${data.processed_filename}?t=${new Date().getTime()}`;
          processedImageContainer.style.display = 'block';
      }).catch(error => {
          console.error('Ошибка при обработке изображения:', error);
      });
}

// Обработчики изменения параметров
document.getElementById('maxValue').addEventListener('input', updateProcessedImageWithCurrentFilename);
document.getElementById('adaptiveMethod').addEventListener('change', updateProcessedImageWithCurrentFilename);
document.getElementById('thresholdType').addEventListener('change', updateProcessedImageWithCurrentFilename);
document.getElementById('blockSize').addEventListener('input', updateProcessedImageWithCurrentFilename);
document.getElementById('C').addEventListener('input', updateProcessedImageWithCurrentFilename);

function updateProcessedImageWithCurrentFilename() {
    if (uploadedFilenames.length > 0) {
        const currentFilename = uploadedFilenames[uploadedFilenames.length - 1];
        updateProcessedImage(currentFilename);
    }
}
