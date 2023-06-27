function buttonClick(){
    let name = prompt("Podaj swoje imię");
    if (name != null) {
        if (name.endsWith('a')){
            document.getElementById("demo").innerHTML =
            "Dzień dobry Pani " + name;
        }
        else{
            document.getElementById("demo").innerHTML =
            "Dzień dobry Panu " + name;
        }
            
    }
}