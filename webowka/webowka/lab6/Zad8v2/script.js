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
    
    let j=0;
    for (let c in products) {
        
        let text = document.createTextNode(c);
        let summary = document.createElement("summary");
        summary.appendChild(text);
        let details = document.createElement("details");
        details.classList.add(c);
        details.appendChild(summary);
        let ul = document.createElement("ul");
        details.appendChild(ul);
        document.body.appendChild(details);

        let ch2 = document.createElement("input");
        ch2.setAttribute("type", "checkbox")
        ch2.id="o"+j;
        summary.appendChild(ch2)
        let i=0;
        for (let p of products[c]) {
            
            
            let text = document.createTextNode(p);
            let li = document.createElement("li");
            let ch = document.createElement("input");
            ch.setAttribute("type", "checkbox")
            ch.id= 'c'+j+i;
            ch.className = 'c'+j
            li.appendChild(ch)
            li.appendChild(text);
            ul.appendChild(li);
            
            

            i++
        }
    
        j++
        
    console.log(summary)
    }

    var co = document.querySelectorAll('[id^=o]')
    
    

    suboptions = []
    for(var i =0;i<co.length;i++){
      var checkboxes = document.querySelectorAll('input.c' + i)
      suboptions.push(checkboxes)
      
    }

    for (let index = 0; index < suboptions.length; index++) {
        for (let j = 0; j < suboptions[index].length; j++) {
            suboptions[index][j].onclick = function() {
            var checkedCount = document.querySelectorAll('input.c' + index +':checked').length;
        
            co[index].checked = checkedCount > 0;
            co[index].indeterminate = checkedCount > 0 && checkedCount < suboptions[index].length;
          }
          
        }
        
      }

      co.forEach(c => {
        c.onclick = function(){
          
          index = c.id.slice(-1);
          for(var k = 0; k< suboptions[index].length; k++){
            suboptions[index][k].checked = this.checked;
          }
  
        }
        
      });
})