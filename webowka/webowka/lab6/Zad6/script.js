import { countries } from "./countries_data.js";
var data = countries;
/*
fetch("./countries_data.js")
.then(res => res.json())
.then(res => {
    data = res
    console.log(data)
    });*/


//a. Lista 10 najpopularniejszych języków swiata ( wraz z iloscia krajów w których się ich używa) 
var lang = []

for (var i = 0;i<data.length;i++){
  for(var j =0; j<data[i].languages.length;j++){
    lang.push(data[i].languages[j])
  }
}

const occurrences = lang.reduce(function (acc, curr) {
  return acc[curr] ? ++acc[curr] : acc[curr] = 1, acc
}, {});

let sortable = [];
for (var l in occurrences) {
    sortable.push([l, occurrences[l]]);
}

sortable.sort(function(a, b) {
    return b[1] - a[1];
});

var a = document.querySelector('#a')



for(var i = 0; i< 10;i++){
  const row = document.createElement('tr');
  row.id = "langg"
  var label = document.createElement('label');
  label.for="langg"
  label.innerHTML = `${sortable[i][0]} ${sortable[i][1]}<br>`
  var m = sortable[i][1]
  m = parseInt(m)
  var l = ""
  for(var j = 0; j<m ; j++){
    l += `<td style="background-color:orange">&nbsp</td>`  ;
  }
  row.innerHTML = l
  a.appendChild(label)
  a.appendChild(row)

}

//b. Lista 10 najmniej popularnych języków swiata
var lang2 =[]
for (var i = 0;i<data.length;i++){
  for(var j =0; j<data[i].languages.length;j++){
    lang2.push([data[i].languages[j], data[i].population])
  }
}

var lann = {}
for (let index = 0; index < lang2.length; index++) {
  if(!Object.keys(lann).includes(lang2[index][0])){
    lann[lang2[index][0]] = lang2[index][1]
  }else{
    lann[lang2[index][0]] += lang2[index][1]
  }
}

var items = Object.keys(lann).map(function(key) {
  return [key, lann[key]];
});

items.sort(function(first, second) {
  return first[1] - second[1];
});

console.log(items.slice(0, 5));

var a = document.querySelector('#b')



for(var i = 0; i< 5;i++){
  const row = document.createElement('tr');
  row.id = "langg"
  var label = document.createElement('label');
  label.for="langg"
  label.innerHTML = `${items[i][0]} ${items[i][1]}<br>`
  var m = items[i][1]/450
  m = parseInt(m)
  console.log(m)
  var l = ""
  for(var j = 0; j<m ; j++){
    l += `<td style="background-color:orange">&nbsp</td>`  ;
  }
  row.innerHTML = l
  a.appendChild(label)
  a.appendChild(row)

}

//c. Lista 5 najpopularniejszych nazw waluty 




var currency = []

for (var i = 0;i<data.length;i++){
  currency.push(data[i].currency)
}
/*
var uniq = [...new Set(curr)];

console.log(uniq)*/

for(var i =0; i<currency.length;i++){
  var str = currency[i].toLowerCase()
  var lastIndex = str.lastIndexOf(" ");
  str = str.substring(lastIndex +1, currency[i].length);
  currency[i] = str
}

const curroccurrences = currency.reduce(function (acc, curr) {
  return acc[curr] ? ++acc[curr] : acc[curr] = 1, acc
}, {});

let sortablev3 = [];
for (var l in curroccurrences) {
    sortablev3.push([l, curroccurrences[l]]);
}

sortablev3.sort(function(a, b) {
    return b[1] - a[1];
});

var a = document.querySelector('#c')



for(var i = 0; i< 5;i++){
  const row = document.createElement('tr');
  row.id = "langg"
  var label = document.createElement('label');
  label.for="langg"
  label.innerHTML = `${sortablev3[i][0]} ${sortablev3[i][1]}<br>`
  var m = sortablev3[i][1]
  m = parseInt(m)
  var l = ""
  for(var j = 0; j<m ; j++){
    l += `<td style="background-color:orange">&nbsp</td>`  ;
  }
  row.innerHTML = l
  a.appendChild(label)
  a.appendChild(row)

}


