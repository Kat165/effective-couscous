/*
var addbtn = document.querySelector(".addbtn");
var listElements = document.getElementById("listElements");


addbtn.onclick = function() {
    let newElement = document.createElement('input')
    document.listElements.appendChild(newElement)
    console.log("xxx")
}
*/
/*

const insert = document.querySelector('#addbtn');
insert.addEventListener('click', () => {
  const subject = document.querySelector('#listElements');
  subject.insertAdjacentHTML('afterbegin', '<strong>inserted text</strong>');
});

const para = document.createElement("p");
const node = document.createTextNode("This is new.");
para.appendChild(node);
const element = document.getElementById("div1");
element.appendChild(para);
*/


var addbtn = document.querySelector("#addbtn");
var listElements = document.getElementById("listElements");


addbtn.onclick = function() {
  /*
    const para = document.createElement("p");
    const node = document.createTextNode("This is new.");
    para.appendChild(node);

    const element = document.getElementById("listElements");
    element.appendChild(para);
    console.log("xxx")*/
    const subject = document.querySelector('#listElements');
    subject.insertAdjacentHTML("afterbegin", '<div><div><p>imie</p><p>nr</p></div><div><button>kosz</button></div></div>');
}


