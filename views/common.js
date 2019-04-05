function app() {

  function start(options) {
    addEventToSubmit()
    addEventToMobileNav()
    addEventToSignOut()
  }

  function addEventToSubmit() {
    let submitButton = document.querySelector('#submit');
    if(submitButton !== null) {
      document.body.addEventListener( 'keyup', function (e) {
        if ( e.keyCode == 13 ) {
          submitAction();
        }
      });

      submitButton.addEventListener('click', function(e) {
        submitAction();
      }, false);
    }
  }

  function submitAction() {
    document.body.style.cursor = 'progress';
    const form = document.querySelector('form');
    let data = Object.values(form).reduce(
      (obj,field) => {
          if (field.name != '' && ((field.type !== 'checkbox' && field.type !== 'radio') || field.checked)) {
              obj[field.name] = field.value;
          }
        return obj
      },
      {}
    );
    console.log(data);
    submitInputs(data)
  }

  function submitInputs(data) {
    var apiUrl = window.location.href ;
    var xhr = new XMLHttpRequest();

    xhr.open('POST', apiUrl);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        if(typeof response.redirect != 'undefined') {
          window.location.href = response.redirect;
        } else {
          console.log(response);
          if(typeof response.body != 'undefined' &&
            typeof response.body.errors != 'undefined') {
            processValidation(response.body.errors);
          }
        }
      }
      document.body.style.cursor = 'default';

    };
    xhr.send(JSON.stringify(data));
  }

  function addEventToMobileNav() {
    let mobileNavButton = document.querySelector('#mobile-nav');
    if(mobileNavButton !== null) {
      mobileNavButton.addEventListener('click', function(e) {
        var mobileNavLinks = document.getElementById("mobile-nav-links");
        if (mobileNavLinks.className.indexOf("w3-show") == -1) {
          mobileNavLinks.className += " w3-show";
        } else {
          mobileNavLinks.className = mobileNavLinks.className.replace(" w3-show", "");
        }
      }, false);
    }
  }

  function addEventToSignOut() {
    let signOut = document.querySelector('#sign-out');
    if(signOut !== null) {
        signOut.addEventListener('click', function(e) {
          document.cookie = "X-token= ; expires = Thu, 01 Jan 1970 00:00:00 GMT"
          window.location.href = 'sign-in';
        }, false);
    }
  }

  function processValidation(errors) {
    let text = '';
    let validationDiv = document.querySelector('#validation-top');
    var elements = document.querySelectorAll('input');

    validationDiv.setAttribute( 'style', 'display:none' );
    while(validationDiv.firstChild) validationDiv.removeChild(validationDiv.firstChild)
    for (let i = 0, element; element = elements[i++];) {
      element.classList.remove('w3-border-red');
    }

    for (let i = 0, error; error = errors[i++];) {
      let field = document.querySelector('input[name="' + error.field + '"]');
      if(field == null) {
          field = document.querySelector('select[name="' + error.field + '"]');
      }
      field.classList.add('w3-border-red');
      var newEl = document.createElement('h4');
      newEl.className = 'w3-center w3-text-white';
      newEl.innerHTML = error.message;
      validationDiv.appendChild(newEl);
    }

    validationDiv.setAttribute( 'style', 'display:block' );
  }

  return {
    start: start
  }

}
