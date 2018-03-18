$( document  ).ready(function() {
  var form = document.querySelector('form[data-stripe-key]');
  if (form === null) {
    return;
  }
  var key = form.getAttribute('data-stripe-key');
  console.log(key);
  if (key) {
    if (Stripe === undefined) {
      throw 'pinax-stripe integration requires that https://js.stripe.com/v3/ is loaded in a script tag in your page.';
    }
    var stripe = Stripe(key);
    var elements = stripe.elements();
    var card = elements.create('card');
    var errorElement = document.getElementById(form.getAttribute('data-card-errors-id'));
    card.mount('#' + form.getAttribute('data-card-mount-id'));

    card.addEventListener('change', function (event) {
      if (event.error) {
        errorElement.textContent = event.error.message;
      } else {
        errorElement.textContent = '';
      }
    });
  }

    // Handle form submission
    sub = {
        subscribe: function (id){
            console.log(id);
            var form = document.querySelector('form[data-stripe-key]');
              if (form === null) {
                return;
              }

              $("#id_plan").val(id);
              form.submit();
                  event.preventDefault();

                  stripe.createToken(card).then(function (result) {
                    if (result.error) {
                      // Inform the user if there was an error
                      errorElement.textContent = result.error.message;
                    } else {
                      var tokenInput = document.createElement('input');
                      tokenInput.setAttribute('type', 'hidden');
                      tokenInput.setAttribute('name', 'stripeToken');
                      tokenInput.setAttribute('value', result.token.id);
                      form.appendChild(tokenInput);
                      console.log(form);
                      form.submit();
                    }
                  });

        }
    }
    // form.addEventListener('submit', function (event) {
    // });
});
