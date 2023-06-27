let startbtn = false;
let stopbtn = true;
let click = 0;
function startclick(){
    startbtn = true;
    stopbtn = false;
}

function stopclick(){
    startbtn = false;
    stopbtn = true;
    click = 0;
    document.getElementById('licznik').innerHTML = click;
}

function testclick(){
    if (startbtn & !stopbtn){
        click = click+1;
        document.getElementById('licznik').innerHTML = click;
    }
}