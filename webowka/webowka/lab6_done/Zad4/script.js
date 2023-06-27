var myInput = document.getElementById("psw");
var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");
var newPsw = document.getElementById("newpsw")

var len = false;
var cap = false;
var spe = false;
var num = false;

// When the user clicks on the password field, show the message box
myInput.onfocus = function() {
  document.getElementById("message").style.display = "block";
}

// When the user clicks outside of the password field, hide the message box
myInput.onblur = function() {
  document.getElementById("message").style.display = "none";
}

// When the user starts to type something inside the password field
myInput.onkeyup = function() {
  // Validate lowercase letters
  //var lowerCaseLetters = /[a-z]/g;
  var specialChars = /\+|\$|\*|-|&|=|%|#|@|!|\^/g;
  if(myInput.value.match(specialChars)) {
    letter.classList.remove("invalid");
    letter.classList.add("valid");
    spe = true;
  } else {
    letter.classList.remove("valid");
    letter.classList.add("invalid");
    spe = false;
}

  // Validate capital letters
  var upperCaseLetters = /[A-Z]/g;
  if(myInput.value.match(upperCaseLetters)) {
    capital.classList.remove("invalid");
    capital.classList.add("valid");
    cap = true;
  } else {
    capital.classList.remove("valid");
    capital.classList.add("invalid");
    cap = false;
  }

  // Validate numbers
  var numbers = /[0-9]/g;
  if(myInput.value.match(numbers)) {
    number.classList.remove("invalid");
    number.classList.add("valid");
    num = true;
  } else {
    number.classList.remove("valid");
    number.classList.add("invalid");
    num = false;
  }

  // Validate length
  if(myInput.value.length >= 8) {
    length.classList.remove("invalid");
    length.classList.add("valid");
    len = true;
  } else {
    length.classList.remove("valid");
    length.classList.add("invalid");
    len = false;
  }
}

newPsw.addEventListener("keypress", function(event) {
    // If the user presses the "Enter" key on the keyboard
    if (event.key === "Enter") {
      event.preventDefault();
      if(myInput.value != newPsw.value){
        alert("Passwords are different");
      }
      else
      if(myInput.value == newPsw.value & len & cap & num & spe){
        alert("Password correct");
      }
      else{
        alert("Password incorrect")
      }
    }
  });