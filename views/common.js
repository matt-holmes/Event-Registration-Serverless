// Script to open and close sidebar
function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
  document.getElementById("myOverlay").style.display = "block";
}

function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
}

// Modal Image Gallery
function onClick(element) {
  document.getElementById("img01").src = element.src;
  document.getElementById("modal01").style.display = "block";
  var captionText = document.getElementById("caption");
  captionText.innerHTML = element.alt;
}


function app() {
  function init(options) {
    addEventToSubmit()
  }

  function addEventToSubmit() {
    let submitButton = document.querySelector('#submit');
    let self = this;
    submitButton.addEventListener('click', function(e) {
        const form = document.querySelector('form');
        let data = Object.values(form).reduce(
            (obj,field) => {
              obj[field.name] = field.value;
              return obj
            },
            {}
          );
        submitInputs(data)
        console.log(data)
    }, false);
  }

  function submitInputs(data) {
    var apiUrl = window.location.href ;
    var xhr = new XMLHttpRequest();

    xhr.open('POST', apiUrl);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
        }
    };
    xhr.send(JSON.stringify(data));
  }

  return {
    init: init
  }

}
