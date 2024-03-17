document.getElementById("sendMessageBtn").addEventListener("click", function() {
    console.log("Отправка запроса в Telegram...");
    // Выполняем AJAX-запрос для отправки сообщения
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/send_message_to_telegram/", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Получаем CSRF-токен из метатега CSRF и добавляем его в данные запроса
    var csrftoken = getCookie('csrftoken'); // Функция getCookie определена ниже
    xhr.setRequestHeader("X-CSRFToken", csrftoken);

    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
            alert("Сообщение успешно отправлено в Telegram!");
        } else {
            alert("Произошла ошибка при отправке сообщения в Telegram.");
        }
    };

    xhr.onerror = function() {
        alert("Произошла ошибка при выполнении запроса.");
    };

    var data = JSON.stringify({
        // Ваши данные для отправки в Telegram
    });
    xhr.send(data);
});

// Функция для получения значения CSRF-токена из cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Проверяем, начинается ли куки с искомого имени
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
