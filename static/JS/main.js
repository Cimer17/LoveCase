const cells = 31;

document.addEventListener('DOMContentLoaded', function() {
    loadItems();
});

function loadItems() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_items', true);

    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 400) {
            var data = JSON.parse(xhr.responseText);
            var list = document.querySelector('.list');
            list.innerHTML = '';

            for (var i = 0; i < 31; i++) {
                var item = data.items[Math.floor(Math.random() * data.items.length)];
                var li = document.createElement('li');
                li.setAttribute('data-item', JSON.stringify(item.name));
                li.classList.add('list__item');
                li.innerHTML = '<img src="' + item.img_url + '" alt="' + item.name + '" />';
                list.appendChild(li);
            }
        } else {
            console.error('Error:', xhr.status);
        }
    };

    xhr.onerror = function() {
        console.error('Request failed');
    };

    xhr.send();
}

function start() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/choose_item', true);

    xhr.onload = function() {
        if (xhr.status >= 200 && xhr.status < 400) {
            var data = JSON.parse(xhr.responseText);
            var winnerIndex = 15; // Индекс победителя
            var items = data.items;
            
            // Получаем список элементов
            var list = document.querySelector('.list');
            
            var listItems = list.querySelectorAll('.list__item');
            listItems.forEach(function(item) {
                item.classList.remove('active');
            });

            // Устанавливаем начальные стили перед обновлением списка
            list.style.transition = 'none';
            list.style.left = '0';
            list.style.transform = 'translate3d(0, 0, 0)';
            
            for (var i = 0; i < 31; i++) {
                var item;
                if (i === winnerIndex) {
                    // Используем данные о победителе
                    item = data.winner;
                } else {
                    // Используем данные об обычном предмете
                    item = items[Math.floor(Math.random() * items.length)];
                }

                var li = list.querySelectorAll('li')[i];
                li.setAttribute('data-item', JSON.stringify(item.name));
                li.innerHTML = '<img src="' + item.img_url + '" alt="' + item.name + '" />';
            }
            
            function transitionEndHandler() {
                var item = list.querySelectorAll('li')[winnerIndex];
                item.classList.add('active');
            }

            // Применяем изменения к DOM перед запуском анимации
            setTimeout(function() {
                list.offsetHeight; // Принудительно обновляем макет для активации анимации
                list.style.transition = ''; // Удаляем инлайн стиль, чтобы активировать анимацию
                list.style.left = '50%';
                list.style.transform = 'translate3d(-50%, 0, 0)';

                list.addEventListener('transitionend', transitionEndHandler, { once: true });
            }, 400);

        } else {
            console.error('HTTP error: ' + xhr.status);
        }
    };

    xhr.onerror = function() {
        console.error('Request failed');
    };

    xhr.send();
}