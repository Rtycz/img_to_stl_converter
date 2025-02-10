// static/js/scripts.js

let uploadedFilenames = []; // Список для хранения имен загруженных файлов

document.getElementById('photoInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        const preview = document.getElementById('preview');
        const loader = document.getElementById('loader');
        const previewImage = document.getElementById('previewImage');

        // Показать индикатор загрузки
        loader.style.display = 'block';
        preview.style.display = 'block';
        previewImage.style.display = 'none';

        reader.onload = function(e) {
            // Отображение превью изображения после загрузки
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
            loader.style.display = 'none';
        };
        reader.readAsDataURL(file);

        // Создание объекта FormData и добавление файла
        const formData = new FormData();
        formData.append('photo', file);

        // Отправка файла на сервер с использованием fetch
        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => response.json())
          .then(data => {
              uploadedFilenames.push(data.filename); // Добавление имени файла в список
          }).catch(error => {
              console.error('Ошибка при загрузке фото:', error);
          });
    }
});

// Обработчик события beforeunload для удаления всех файлов при закрытии вкладки
window.addEventListener('beforeunload', function(event) {
    if (uploadedFilenames.length > 0) {
        // Уведомление сервера об удалении всех файлов
        fetch('/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filenames: uploadedFilenames })
        }).then(response => response.text())
          .then(data => {
              console.log(data);
          }).catch(error => {
              console.error('Ошибка при удалении фото:', error);
          });
    }
});
