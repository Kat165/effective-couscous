var data = [];
/*
async function fetchProducts(){
  const p1 = await fetch("http://localhost:3000/Produkty")
  return p1
}
fetchProducts().then(res => res.json())
  .then(res => {
    data = res
    });*/

fetch("http://localhost:3000/Produkty")
    .then(res => res.json())
    .then(res => {
      data = res
      });

/*
async function fetchProducts() {
    const kat = await fetch("./kategorie.json");
    const p1 = await fetch("./produktyA.json");
    const p2 = await fetch("./produktyB.json");
    const c = await kat.json();
    const data = await p1.json();
    const pr2 = await p2.json();
    return [c, data, pr2];
}


async function fetchProducts() {
  const kat = await fetch("./kategorie.json");
  const p1 = await fetch("./produktyA.json");
  const p2 = await fetch("./produktyB.json");
  const c = await kat.json();
  const pr1 = await p1.json();
  const pr2 = await p2.json();
  return [c, pr1, pr2];
}


fetchProducts().then(res => {
  let products = {};
  for (let c in res[0]) {
      products[res[0][c]] = [];
  }
  console.log(products);
  let fetchedProducts = [res[1], res[2]]    
  for (let d in fetchedProducts) {
      for (let c in fetchedProducts[d]) {
          for (let p of fetchedProducts[d][c]) {
              if (!products[c].includes(p)) {
                  products[c].push(p);
              }
          }
      }
  }
})

  */

function myFunction(){
  console.log(data)
    for(var i = 0; i<data.length; i++){
        const list_menu = document.querySelector('#menu');
    
        var checkbox = document.createElement('input');
        checkbox.type = "checkbox"
        checkbox.id = "option"+i;
        var label = document.createElement('label');
        label.for="option"
        label.id = "lab" +i
        label.innerHTML = `${data[i].type}<br>`
        var list = document.createElement("ul")
        list.id = "list"+i
    
        for(var j = 0; j< data[i].items.length; j++){
            var listel = document.createElement("li")
            
            var cc = document.createElement("input")
            cc.type = "checkbox"
            cc.id = "sub"+i+j
            cc.className="subOption"+i
            var labelcc = document.createElement('label');
            labelcc.for="sub"+i+j
            labelcc.id = "lab"+i+j
            labelcc.innerHTML = `${data[i].items[j]}`
            listel.appendChild(cc)
            listel.appendChild(labelcc)
            list.appendChild(listel)
        }
    
        list_menu.appendChild(checkbox)
        list_menu.appendChild(label)
        list_menu.appendChild(list)
    }

    myFunction2()
    myFunction3()
}
function myFunction2(){
    checkall = document.querySelectorAll('[id^=option]')
    chacks = []



    for(var i =0;i<checkall.length;i++){
      var checkboxes = document.querySelectorAll('input.subOption' + i)
      chacks.push(checkboxes)
      
    }


    for (let index = 0; index < chacks.length; index++) {
      for (let j = 0; j < chacks[index].length; j++) {
          chacks[index][j].onclick = function() {
          var checkedCount = document.querySelectorAll('input.subOption' + index +':checked').length;
      
          checkall[index].checked = checkedCount > 0;
          checkall[index].indeterminate = checkedCount > 0 && checkedCount < chacks[index].length;
          if(chacks[index][j].checked){
            var label = document.querySelector('#lab'+index+j)
            const gl = document.querySelector('#gl-list');
            var listel = document.createElement("li")
            listel.innerHTML = `${label.innerHTML}`
            gl.appendChild(listel)


          }
        }
        
      }
      
    }

    checkall.forEach(c => {
      c.onclick = function(){
        
        index = c.id.slice(-1);
        for(var k = 0; k< chacks[index].length; k++){
          chacks[index][k].checked = this.checked;
          if(chacks[index][k].checked){
            var label = document.querySelector('#lab'+index+k)
            const gl = document.querySelector('#gl-list');
            var listel = document.createElement("li")
            listel.innerHTML = `${label.innerHTML}`
            gl.appendChild(listel)
          }
        }
      }
    });

}

function myFunction3(){
  var labels = document.querySelectorAll('[id^=lab]')
  var lists = document.querySelectorAll('[id^=list]')

  labels.forEach(l =>{
    l.onclick = function(){
      index = l.id.slice(-1)
    
      if (lists[index].style.display === "none") {
        lists[index].style.display = "block";
      } else {
        lists[index].style.display = "none";
      }
    }
    
  })
}

