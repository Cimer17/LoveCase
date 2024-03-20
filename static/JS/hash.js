function checkHash() {
    var xhr = new XMLHttpRequest();
    var hashValue = document.getElementById('hash').value; // Получаем значение хеша из поля ввода
    xhr.open('GET', '/provablyfair/?hash=' + hashValue, true); // Отправляем GET-запрос с параметром hash
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 400) {
            var data = JSON.parse(xhr.responseText);
            var resultDiv = document.getElementById('result');
            if ('user' in data) {
                // Очищаем содержимое результата перед отображением новой информации
                resultDiv.innerHTML = '';
                // Отображаем информацию о пользовательском элементе
                resultDiv.innerHTML += 'Пользователь: ' + data.user + 'Предмет: ' + data.item + ', Кейс: ' + data.case + '<br>';
                resultDiv.innerHTML += 'Client Seed: ' + data.client_seed + ', Server Seed: ' + data.server_seed + ', Nonce: ' + data.nonce + '<br>';
            } else {
                // Если записей с таким хешем нет, отображаем соответствующее сообщение
                resultDiv.innerHTML = 'Об этом хэше нет информации...';
            }
        } else {
            console.error('Ошибка запроса: ' + xhr.status);
        }
    };
    xhr.onerror = function () {
        console.error('Ошибка запроса');
    };
    xhr.send();
}
window.onload = function() {
    var urlParams = new URLSearchParams(window.location.search);
    document.getElementById('hash').value = urlParams.get('hash') || '';
};