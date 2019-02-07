function app() {

  function start(options) {
    addEventToSubmit()
    addEventToMobileNav()
    addEventToSignOut()
  }

  function addEventToSubmit() {
    let submitButton = document.querySelector('#submit');
    if(submitButton !== null) {
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
        }, false);
    }
  }

  function submitInputs(data) {
    var apiUrl = window.location.href ;
    var xhr = new XMLHttpRequest();

    xhr.open('POST', apiUrl);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            window.location.href = response.redirect;
        }
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

  return {
    start: start
  }

}
