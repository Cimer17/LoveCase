const cells = 31;
let isStarted = false;

document.addEventListener('DOMContentLoaded', function() {
    generateItemsFromDatabase();
});

function generateItemsFromDatabase() {
    fetch('/get_items')
        .then(response => response.json())
        .then(data => {
            generateItems(data.items);
        })
}

function generateItems(items) {
    const list = document.querySelector('.list');
    list.innerHTML = '';
    for (let i = 0; i < cells; i++) {
        const item = items[Math.floor(Math.random() * items.length)];
        const li = document.createElement('li');
        li.setAttribute('data-name', item.name);
        li.classList.add('list__item');
        const img = document.createElement('img');
        img.src = item.img_url;
        img.alt = item.name;
        li.appendChild(img);
        list.append(li);
    }
}

function start() {
  if (isStarted) return;
  else isStarted = true;
  
  fetch('/choose_item')
      .then(response => response.json())
      .then(data => {
          const winner = data.winner;
          const allItems = data.items;
          const list = document.querySelector('.list');
          
          setTimeout(() => {
              list.style.left = '50%';
              list.style.transform = 'translate3d(-50%, 0, 0)';
              generateItems(allItems);

              const chosenItemElement = list.querySelector('[data-name="' + winner.name + '"]');
              
              if (chosenItemElement) {
                  chosenItemElement.classList.add('active');
              } else {
                  console.error('Chosen item element not found:', winner.name);
              }
          }, 0);
      })
      .finally(() => {
          isStarted = false;
      });
}