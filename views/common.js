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
