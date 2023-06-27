var modalEle = document.querySelector(".modal");

var modalImage = document.querySelector(".modalImage");

var span = document.getElementsByClassName("close")[0];


Array.from(document.querySelectorAll(".ImgThumbnail")).forEach(item => {
    item.addEventListener("click", event => {
        modalEle.style.display = "block";
        modalImage.src = event.target.src;
    });
});
/*
document.querySelector(".close").addEventListener("click", () => {
    modalEle.style.display = "none";
});


span.onclick = function() {
    modalEle.style.display = "none";
    console.log("xxx")
}
*/
modalEle.onclick = function(event) {
    if (event.target != modalImage) {
        modalEle.style.display = "none";
        console.log("xxx")
    }
}