document.getElementById("sendMessageBtn").addEventListener("click", function() {
    // Выполняем AJAX-запрос для отправки сообщения
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/send_message_to_telegram/", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Получаем CSRF-токен из метатега CSRF и добавляем его в данные запроса
    var csrftoken = getCookie('csrftoken'); // Функция getCookie определена ниже
    xhr.setRequestHeader("X-CSRFToken", csrftoken);

    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 300) {
            var responseData = JSON.parse(xhr.responseText);
            if ("error" in responseData) {
                alert(responseData.error);
            } else {
                alert(responseData.message); // Вывод успешного сообщения
            }
        } else {
            alert("Ошибка вывода!");
        }
    };

    xhr.onerror = function() {
        alert("Ошибка вывода!");
    };
    xhr.send();
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
