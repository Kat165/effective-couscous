let MyList = document.getElementById('list');
let i = 0;
function addbuttonClick(){
    var li = document.createElement("li");
    let text = prompt("Dodaj nowy element listy");
    li.appendChild(document.createTextNode(text));
    li.setAttribute("id", i);
    MyList.appendChild(li);
    i = i+1;
}
let j = 0;
function delbuttonClick(){
    var item = document.getElementById(j);
    MyList.removeChild(item);
    j = j+1;
}
