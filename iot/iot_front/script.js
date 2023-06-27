var temp = document.getElementById("temp");
var settemp = document.getElementById("settemp");
var ota = document.getElementById("ota");
var sleep = document.getElementById("sleep");
var on = document.getElementById("on");
//var off = document.getElementById("off");
var reset = document.getElementById("reset");
var ext = document.getElementById("ext");
var relay1 = document.getElementById("relay1");
var start = document.getElementById("start");
var running = false;
var sleeping = false;
const URL='http://localhost:8080/';


//tabs = [["Temperature"],["Temp_setpoint"],["x"]]
tabs = [["Temperature"],["Temp_setpoint"]]
//tabs = [[],[]]
cats = []

var chart = bb.generate({
    bindto: "#chart",
    type: "area",
    size: {
        height: 600,
        width: 1200
    },
    background: {
        color: "white"
    },
    data: {
        //x: "x",
        columns: tabs,
        types: {
            Temperature: "area-spline",
            Temp_setpoint: "step"
        },
        colors: {
            Temperature: "blue",
            Temp_setpoint: "green"
        }
    },
    axis:{
        x: {
            label: "Czas",
            type: "category",
            categories: cats
        },
        y: {
            label: "Temperatura"
        }
    }
});

var x = 0;
var y = 0;
setInterval(()=>{
    if(!running) return
    if(sleeping) return
    x+=1

    //chart
    var Http = new XMLHttpRequest();
    var url = URL+"temp"
/*
    if(tabs[0].length>=10){
        var del1 = tabs[0][1]
        var del2 = tabs[1][1]
        //var del3 = 
        tabs[0].shift()
        tabs[1].shift()
        cats.shift()
    }*/

    Http.addEventListener("load", () => {
        if (Http.status === 200) {
            var tt
            if(Http.response>500){
                return
            }
            if(Http.response == "")
                tt = 0
            else
                tt = Http.response
            tabs[0].push(tt)
            tabs[1].push(y)
            var today = new Date();
            var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
            var t = time.toString()

            cats.push(t)
            console.log(cats)
            chart.load({
                columns:tabs,
                categories:cats
            })
        }
    });
    
    Http.addEventListener("error", () => {
        alert("Niestety nie udało się nawiązać połączenia");
    });

    Http.open("GET", url, true);
    Http.send();

    //ext
    var Http2 = new XMLHttpRequest();
    var url2 = URL+"ext_adc"

    Http2.addEventListener("load", () => {
        //tutaj możemy też sprawdzać inne statusy - np. 404, 500
        if (Http2.status === 200) {
            ext.innerHTML = "ext adc: " +  Http2.response
        }
    });
    
    Http2.addEventListener("error", () => {
        alert("Niestety nie udało się nawiązać połączenia");
    });
    Http2.open("GET", url2, true);
    Http2.send();

    //relay1
    var Http3 = new XMLHttpRequest();
    var url3 = URL+"relay1"

    Http3.addEventListener("load", () => {
        //tutaj możemy też sprawdzać inne statusy - np. 404, 500
        if (Http3.status === 200) {
            relay1.innerHTML = "relay: " +  Http3.response
        }
    });
    
    Http3.addEventListener("error", () => {
        alert("Niestety nie udało się nawiązać połączenia");
    });
    Http3.open("GET", url3, true);
    Http3.send();

    
},2000)


on.onclick = function(){
    const Http9 = new XMLHttpRequest();
    Http9.open("POST", 'http://localhost:8080/relay0');
    Http9.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); //<- ważne
    

    
    if(running){
        running = false
        on.innerHTML = "ON"
        alert("Wyłączono")
        Http9.send(JSON.stringify({"status": "off"}))

    }
    else{
        running = true
        on.innerHTML = "OFF"
        alert("Włączono")
        Http9.send(JSON.stringify({"status": "on"}))
    }
    Http9.onreadystatechange = (e) => {
        var hr = Http9.response
    }

    var today = new Date();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var t = time.toString()
    start.innerHTML = "Start: "+t
        
}

ota.onclick = function(){
    const Http8 = new XMLHttpRequest();
    Http8.open("GET", 'http://localhost:8080/ota');
    Http8.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); //<- ważne
    Http8.send()

    Http8.onreadystatechange = (e) => {
        var hr = Http8.response
    }
    alert("Włączono OTA")
}

sleep.onclick = function(){
    
    if(!sleeping){
        alert("Uśpiono")
        sleeping = true
    }
    else{
        alert("Wybudzono")
        sleeping = false
    }
    const Http7 = new XMLHttpRequest();
    Http7.open("GET", 'http://localhost:8080/sleep');
    //Http7.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); //<- ważne
    Http7.send()

    Http7.onreadystatechange = (e) => {
        var hr = Http7.response
        console.log(hr)
    }
    
}

reset.onclick = function(){
    
    const Http6 = new XMLHttpRequest();
    Http6.open("GET", 'http://localhost:8080/reset');
    Http6.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); //<- ważne
    Http6.send()

    Http6.onreadystatechange = (e) => {
        var hr = Http6.response
    }
    alert("Zresetowano hasło!")
}

settemp.onclick = function(){
    var new_temp = temp.value
    new_temp = Math.round(new_temp)
    if(new_temp>500 || new_temp<0){
        alert("Dopuszczalny zakres temperatury: 0 - 500 stopni! Zmień temperaturę")
        return
    }
    y = new_temp
    

    const Http5 = new XMLHttpRequest();
    Http5.open("POST", 'http://localhost:8080/setpoint');
    Http5.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); //<- ważne
    Http5.send(JSON.stringify({"temp": new_temp}))

    Http5.onreadystatechange = (e) => {
        var hr = Http5.response
    }
    alert("Pomyślnie ustawiono temperaturę " + new_temp + " stopni")


    
}

