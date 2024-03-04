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
            
            // Создание списка элементов
            var list = document.querySelector('.list');
            list.innerHTML = '';

            for (var i = 0; i < 31; i++) {
                var item;
                if (i === winnerIndex) {
                    // Используем данные о победителе
                    item = data.winner;
                } else {
                    // Используем данные об обычном предмете
                    item = items[Math.floor(Math.random() * items.length)];
                }

                var li = document.createElement('li');
                li.setAttribute('data-item', JSON.stringify(item.name));
                li.classList.add('list__item');
                li.innerHTML = '<img src="' + item.img_url + '" alt="' + item.name + '" />';
                list.appendChild(li);
            }

            // Устанавливаем стили и обработчик события transitionend
            setTimeout(function() {
                list.style.left = '50%';
                list.style.transform = 'translate3d(-50%, 0, 0)';

                list.addEventListener('transitionend', function() {
                    var item = list.querySelectorAll('li')[winnerIndex];
                    item.classList.add('active');
                    var winnerData = data.winner;
                    console.log(winnerData);
                }, { once: true });
            }, 100);
        } else {
            console.error('HTTP error: ' + xhr.status);
        }
    };

    xhr.onerror = function() {
        console.error('Request failed');
    };

    xhr.send();
}



// function generateItems(items) {

//     function getItem(){
//         let item;

//         while (!item) {
//             const chance = Math.floor(Math.random() * 100)
//             console.log(chance)
//             items.forEach(elm => {
//                 if (chance < elm.chance && !item) item = elm
//                 console.log(elm.chance)
//             })
//         }

//         return item
//     }

//     document.querySelector('.list').remove()
//     document.querySelector('.scope').innerHTML = `
//     <ul class="list"></ul>
//     `
    
//     const list = document.querySelector('.list')

//     for (let i = 0; i < cells; i++) {

//         const item = getItem();

//         const li = document.createElement('li')
//         li.setAttribute('data-item', JSON.stringify(item))
//         li.classList.add('list__item')
//         li.innerHTML = `
//             <img src="${item.img_url}" alt="" />
//         `
    
//         list.append(li)
//     }
// }
    

// // fetch('/get_items')
// // .then( response => {
// //     if (!response.ok) {
// //     throw new Error(`HTTP error: ${response.status}`);
// //     }
// //     return response.json();
// // })
// // .then( data => { generateItems(data.items) })
// // .catch( err => console.error(`Fetch problem: ${err.message}`) );


// let isStarted = false
// let isFirstStart = true

// function start() {
//     if (isStarted) return
//     else isStarted = true

//     if (!isFirstStart){
//         fetch('/get_items')
//         .then( response => {
//             if (!response.ok) {
//             throw new Error(`HTTP error: ${response.status}`);
//             }
//             return response.json();
//         })
//         .then( data => { generateItems(data.items) })
//         .catch( err => console.error(`Fetch problem: ${err.message}`) );
//         console.log("меня нет")
//     }
//     else isFirstStart = false
//     setTimeout(() => {
//         const list = document.querySelector('.list');

//         console.log(list)

//         list.style.left = '50%'
//         list.style.transform = 'translate3d(-50%, 0, 0)'
        
//         const item = list.querySelectorAll('li')[15]

//         console.log("меня нет пока что")
//         console.log(item)
    
//         list.addEventListener('transitionend', () => {
//             isStarted = false
//             item.classList.add('active')
//             const data = JSON.parse(item.getAttribute('data-item'))
            
//             console.log(data);
//         }, {once: true})
//     }, 100)
// }