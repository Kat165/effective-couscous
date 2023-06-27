let MyLmage = document.querySelector('img');


MyLmage.onclick = function(){
    let mySrc = MyLmage.getAttribute('src')
    if(mySrc === "img/gora.jpg"){
        MyLmage.setAttribute('src',"img/las2.jpg")
        MyLmage.setAttribute('style',"border:green; border-width:5px; border-style:solid;")
    }else if(mySrc === "img/las2.jpg"){
        MyLmage.setAttribute('src',"img/morze.jpg")
        MyLmage.setAttribute('style',"border:blue; border-width:5px; border-style:solid;")
    }else{
        MyLmage.setAttribute('src',"img/gora.jpg")
        MyLmage.setAttribute('style',"border:red; border-width:5px; border-style:solid;")
    }
}