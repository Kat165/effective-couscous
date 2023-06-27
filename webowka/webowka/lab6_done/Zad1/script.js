var div1 = document.querySelector('#id1')
var div2 = document.querySelector('#id2')
var div3 = document.querySelector('#id3')
var list = document.querySelector('#list')
var points = document.querySelector('#points')
//var divall = document.querySelectorAll('[id^=id]')
var st = document.querySelector('#st')
var re = document.querySelector('#re')
var zm = document.querySelector('#zm')
var cont = document.querySelector('#cont');
var point = 0;
div1.style.pointerEvents = "none";
div2.style.pointerEvents = "none";
div3.style.pointerEvents = "none";


div1.onclick = function(e){
    var listel = document.createElement('li')
    listel.innerHTML = `Nacisnąłeś niebieski o wartości 1`
    list.appendChild(listel)
    point +=1
    points.innerHTML = `Points: ${point}`
    if (!e) var e = window.event;
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();
    if(point+1>30){
        div2.style.backgroundColor = "gray";
    }
    if(point+1>50){
        div3.style.backgroundColor = "gray";
    }

}

div2.onclick = function(e){
    if(point<30){
        var listel = document.createElement('li')
        listel.innerHTML = `Nacisnąłeś czerwony o wartości 2`
        list.appendChild(listel)
        point +=2
        points.innerHTML = `Points: ${point}`
        if (!e) var e = window.event;
        e.cancelBubble = true;
        if (e.stopPropagation) e.stopPropagation();
    }else{
        div2.style.backgroundColor = "gray";
    }
    
}

div3.onclick = function(e){
    console.log(point)
    if(point+5>30){
        div2.style.backgroundColor = "gray";
    }
    if(point<50){
        var listel = document.createElement('li')
        listel.innerHTML = `Nacisnąłeś żółty o wartości 5`
        list.appendChild(listel)
        point +=5
        points.innerHTML = `Points: ${point}`
        if (!e) var e = window.event;
        e.cancelBubble = true;
        if (e.stopPropagation) e.stopPropagation();
    }else{
        div3.style.backgroundColor = "gray";
    }
   
}

st.onclick = function(){    
    if(div1.style.pointerEvents === "none"){
        st.innerHTML = `Start`
        div1.style.pointerEvents = "auto";
        div2.style.pointerEvents = "auto";
        div3.style.pointerEvents = "auto";
    }else{
        st.innerHTML = `Stop`
        div1.style.pointerEvents = "none";
        div2.style.pointerEvents = "none";
        div3.style.pointerEvents = "none";
    }
}

re.onclick = function(){
    list.innerHTML = ``;
    point = 0;
    points.innerHTML = `Points: ${point}`
    div2.style.backgroundColor = "red";
    div3.style.backgroundColor = "yellow";

}






