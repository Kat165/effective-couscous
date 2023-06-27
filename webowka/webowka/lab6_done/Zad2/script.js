class Number{
    constructor(name,number){
        this.name = name;
        this.number = number;
    }
}

class UI{
    static showNumbs(){
        
        const nums = Store.getNums();

        nums.forEach((num) => UI.addNumToList(num));

    }

    static addNumToList(number) {
        const list = document.querySelector('#number-list');

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${number.name}</td>
            <td>${number.number}</td>
            <td><a href = "#" style="text-decoration:none " class="delete">&#10006;</a></td> </tr>
        `;

        list.appendChild(row);
    }

    static deleteNumber(target){
        if(target.classList.contains('delete')){
            target.parentElement.parentElement.remove();
        }
    }

    static showAlert(message, color){
        const div = document.createElement('div');
        div.className = `alert`;
        div.appendChild(document.createTextNode(message));
        const container = document.querySelector('.container')
        const tab = document.querySelector('#myTable');
        container.insertBefore(div,tab);
    }

    static clerFields(){
        document.querySelector("#name").value = '';
        document.querySelector("#number").value = '';
    }
}

class Store{
    static getNums(){
        let numbers;
        if(localStorage.getItem('numbers')==null){
            numbers = [];
        }else{
            numbers = JSON.parse(localStorage.getItem('numbers'));
        }
        return numbers;

    }

    static addNum(number){
        const numbers = Store.getNums();

        numbers.push(number);

        localStorage.setItem('numbers',JSON.stringify(numbers));
    }

    static removeNum(num){
        const numbers = Store.getNums();
        numbers.forEach((number,index)=>{
            if(number.number == num){
                numbers.splice(index,1);
            }
        });

        localStorage.setItem('numbers',JSON.stringify(numbers));
    }
}

document.addEventListener('DOMContentLoaded',UI.showNumbs);

document.querySelector('#addForm').addEventListener('submit',(e)=>{

    e.preventDefault();

    const name = document.querySelector('#name').value;
    const number = document.querySelector('#number').value;

    var phoneno = /^[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*$/;
    var phoneno2 = /^\+\s*[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*[0-9]\s*[0-9]*\s*[0-9]\s*[0-9]\s*[0-9]$/;
    if(!number.match(phoneno) && !number.match(phoneno2)){
        alert("Wrong number format");
        return
    }

    //var nameno = /^[A-Z][a-z]*\s[A-Z][a-z]*/
    var nameno = /^[A-Z][a-z]*( [A-Z][a-z]*([-]?[A-Z][a-z]+)?)$/
    if(!name.match(nameno)){
        alert("Wrong name format");
        return
    }


    const newnumber = new Number(name,number);

    UI.addNumToList(newnumber);

    Store.addNum(newnumber);

    UI.clerFields()

});

document.querySelector('#number-list').addEventListener('click',(e)=>{
    UI.deleteNumber(e.target);

    Store.removeNum(e.target.parentElement.previousElementSibling.textContent);
});