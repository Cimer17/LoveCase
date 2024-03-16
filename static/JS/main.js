const cells = 31;

function get_id_case(){
    var url_text = String(document.location.pathname);
    return url_text.slice(6, url_text.length - 1);
}


document.addEventListener('DOMContentLoaded', function() {
    loadItems();
});

function loadItems() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/get_items?id=${get_id_case()}`, true);

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
                li.classList.add('gradient_' + item.rare);
                li.innerHTML = '<img src="' + item.img_url + '" alt="' + item.name + '" />' + '<p>' + item.name + '</p>';
                list.appendChild(li);
            }
            // Добавляем проверку на значение end и скрываем кнопку, если предметы закончились
            if (data.end) {
                document.querySelector('.start').classList.add('hidden');
                document.querySelector('.case-ended-message').classList.remove('hidden');
            } else {
                document.querySelector('.start').classList.remove('hidden');
                document.querySelector('.case-ended-message').classList.add('hidden');
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
    var audio = document.getElementById("audio_open");
    var game = document.getElementById("audio_open_start");
    var win = document.getElementById('audio_win');
    audio.play();
    game.play();
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/choose_item?id=${get_id_case()}`, true);

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

                var existingGradientClasses = li.className.match(/gradient_\d+/g);
                if (existingGradientClasses) {
                    existingGradientClasses.forEach(function(className) {
                        li.classList.remove(className);
                    });
                }

                var gradientClass;
                switch (item.rare) {
                    case 1:
                        gradientClass = 'gradient_1';
                        break;
                    case 2:
                        gradientClass = 'gradient_2';
                        break;
                    case 3:
                        gradientClass = 'gradient_3';
                        break;
                    case 4:
                        gradientClass = 'gradient_4';
                        break;
                    case 5:
                        gradientClass = 'gradient_5';
                        break;
                    case 6:
                        gradientClass = 'gradient_6';
                        break;
                    default:
                        gradientClass = 'gradient_default'; // Если значение item.rare не соответствует ни одному из значений выше
                }
                li.classList.add('list__item', gradientClass);
                li.setAttribute('data-item', JSON.stringify(item.name));
                li.innerHTML = '<img src="' + item.img_url + '" alt="' + item.name + '" />' + '<p>' + item.name + '</p>';
            }

            document.querySelector('.case').classList.add('hidden');
            document.querySelector('.start').classList.add('hidden');
            document.querySelector('.pointer').classList.remove('hidden');
            document.querySelector('.scope').classList.remove('hidden');

            function transitionEndHandler() {
                var item = list.querySelectorAll('li')[winnerIndex];
                item.classList.add('active');
                document.querySelector('.start').classList.remove('hidden');
                win.play();

                // Обновляем или создаем ссылку на хеш
                var hashLink = document.getElementById('hashLink');
                if (hashLink) {
                    hashLink.setAttribute('href', data.link_hash);
                } else {
                    var hashLinkContainer = document.createElement('div');
                    hashLinkContainer.innerHTML = '<a  target="_blank" id="hashLink" href="' + data.link_hash + '">hash_link</a>';
                    document.body.appendChild(hashLinkContainer);
                }
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



