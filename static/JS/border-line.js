const divElement = document.querySelector('.box-text');
const textBox = document.querySelector('.text-about');
const column = document.querySelectorAll('.border');
const boxSize = document.querySelector('.tempClass');

const ro = new ResizeObserver((enteries) => {
    for( const entry of enteries){
        let heights = entry.target.offsetHeight;
        let sHeigt = Math.round(heights * 0.125);
        let sHeigts = Math.round((heights * 0.35)+heights);

        if(heights <= 400){
            for(let sTemp of column){
                if(heights >= 140 && 
                    heights <= 400)
                {
                    sTemp.style.height = `${sHeigt}px`;
                    sTemp.style.width = `${sHeigt}px`;
                    boxSize.style.height = `${sHeigts}px`;
                }

                console.log(heights)
            }
        }
    }
});

document.addEventListener('DOMContentLoaded', function(){
    if(textBox){ 
        ro.observe(divElement);
        console.log("Инициализация выполнена!")
    }
    else console.log("Инициализация не выполнена!")
});