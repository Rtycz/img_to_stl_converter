// static/js/scripts.js

let uploadedFilename = ''; // Переменная для хранения имени загруженного файла

document.getElementById('photoInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            // Отображение превью изображения
            document.getElementById('previewImage').src = e.target.result;
            document.getElementById('preview').style.display = 'block';
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
              uploadedFilename = data.filename; // Сохранение имени загруженного файла
          }).catch(error => {
              console.error('Ошибка при загрузке фото:', error);
          });
    }
});

// Обработчик события beforeunload для удаления файла при закрытии вкладки
window.addEventListener('beforeunload', function(event) {
    if (uploadedFilename) {
        // Уведомление сервера об удалении файла
        fetch('/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: uploadedFilename })
        }).then(response => response.text())
          .then(data => {
              console.log(data);
          }).catch(error => {
              console.error('Ошибка при удалении фото:', error);
          });
    }
});
