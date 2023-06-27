var data = [];

fetch("http://localhost:3000/cities")
.then(res => res.json())
.then(res => {
    data = res
    });


   
var show = document.querySelector("#show");

show.onclick = function(){
    var miasta =data.filter((str) => str.province.toLowerCase().includes("małopolskie"))
    const list = document.querySelector('#list');

    for(let i = 0;i< miasta.length;i++){
        const row = document.createElement('li');
        row.innerHTML = `${miasta[i].name}`
        list.appendChild(row);
    }
  
}

var showv2 = document.querySelector("#showv2");

showv2.onclick = function(){
    const regex = new RegExp('/a/');
    var miasta =data.filter((str) => ((str.name.toLowerCase().match(/[^a]*a[^a]*a[^a]*$/))));
    var miasta3 =data.filter((str) => ((str.name.toLowerCase().match(/[^a]*a[^a]*a[^a]*a[^a]*$/))));
    console.log(miasta3)
    const list = document.querySelector('#listv2');
    var miasta3name = []
    for(let i = 0;i< miasta3.length;i++){
        miasta3name.push(miasta3[i].name)
    }


    for(let i = 0;i< miasta.length;i++){
        const row = document.createElement('li');
        if(!(miasta3name.includes(miasta[i].name))){
            row.innerHTML = `${miasta[i].name}`
            list.appendChild(row);
        }
        
    }

}



var showv3 = document.querySelector("#showv3");

showv3.onclick = function(){
    var miasta =data.sort((a,b) => b.density - a.density);
    const list = document.querySelector('#listv3');

    const row = document.createElement('li');
    row.innerHTML = `${miasta[4].name} ${miasta[4].density}`
    list.appendChild(row);

}

var showv4 = document.querySelector("#showv4");

showv4.onclick = function(){
    var miasta =data
    const list = document.querySelector('#listv4');

    for(let i =0;i<miasta.length;i++){
        if(miasta[i].people>100000){
            miasta[i].name = miasta[i].name + " city"
        }

        const row = document.createElement('li');
        row.innerHTML = `${miasta[i].name} ${miasta[i].people}`
        list.appendChild(row);
    }
}

var showv5 = document.querySelector("#showv5");

showv5.onclick = function(){
    var miasta = data
    const list = document.querySelector('#listv5');

    let a = 0;
    let b = 0;

    for(let i =0;i<miasta.length;i++){
        if(miasta[i].people>80000){
            a++;
        }
        else{
            b++
        }
    }

    const row = document.createElement('li');
        

    if(a>b){
        row.innerHTML = `Więcej jest miast o większej liczbie mieszkańców niż 80000 (${a}), miast o mniejszej liczbie mieszkańców jest ${b}`
    }
    if(b>a){
        row.innerHTML = `Więcej jest miast o mniejszej liczbie mieszkańców niż 80000 (${b}), miast o większej liczbie mieszkańców jest ${a}`
    }
    else{
        row.innerHTML = `Jest tyle samo miast mniejszych i większych (${a} i ${b})`
    }

    list.appendChild(row);

}

var show6 = document.querySelector("#showv6");

show6.onclick = function(){
    var miasta =data.filter((str) => str.province.toLowerCase().startsWith("p"))
    const list = document.querySelector('#listv6');

    console.log(miasta)

    let sum = 0;

    for(let i = 0;i< miasta.length;i++){

        sum += miasta[i].area
    }

    sum = sum/miasta.length

    const row = document.createElement('li');
    row.innerHTML = `${sum}`
    list.appendChild(row);
  
}

var showv7 = document.querySelector("#showv7");

showv7.onclick = function(){
    var miasta =data.filter((str) => str.province.toLowerCase() =="pomorskie")
    const list = document.querySelector('#listv7');

    var sum = 0;
    var sum2 = 0

    for(let i = 0;i< miasta.length;i++){

        if(miasta[i].people>5000){
            sum++;
        }
        else{
            sum2++;
        }
    }
    const row = document.createElement('li');

    if(sum2>0 && sum>0){
        row.innerHTML = `Nie wszystkie miasta są większe niż 5000, miast większych jest ${sum}, a mniejszych ${sum2}`
    }else
    if(sum2 == 0){
        row.innerHTML = `Wszystkie miasta są większe niż 5000, jest ich ${sum}`
    }
    else{
        row.innerHTML = `Wszystkie miasta są mniejsze niż 5000, jest ich ${sum2}`
    }

    list.appendChild(row);
  
}