
        function checkHash() {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/provablyfair/?' + new URLSearchParams(new FormData(document.getElementById('hashForm'))), true);
            xhr.onload = function () {
                if (xhr.status >= 200 && xhr.status < 400) {
                    var data = JSON.parse(xhr.responseText);
                    var resultDiv = document.getElementById('result');
                    if (data.result === 'OK') {
                        resultDiv.innerHTML = 'Хеш верен';
                    } else {
                        resultDiv.innerHTML = 'Хеш неверен';
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
            document.getElementById('username').value = urlParams.get('username') || '';
            document.getElementById('chosen_item_id').value = urlParams.get('chosen_item_id') || '';
            document.getElementById('case_id').value = urlParams.get('case_id') || '';
        };