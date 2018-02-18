$( document  ).ready(function() {
    function  new_account_callback(response){
        if (response.success === true){

            type = 'success',
            html = 'Account saved successfully.'
        } else {
            type = 'warning',
            html = 'Could not save account.'

        }
                        swal({
                            type: type,
                            html: html,
                            confirmButtonClass: 'btn btn-success btn-fill',
                            buttonsStyling: false

                        }).then(function(result){
                            location.reload();
                        })

    }

    function save_new_account(username, password, callback){
        if (username && password){
            $.ajax({
                url: "/ajax/new/fbaccount/",
                method: "POST",
                data: {csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    username: username,
                    password: password },
                success: callback

            });
        }
    }


    app = {
        show_swal: function (type, data){
            if(type == "new-account"){

                swal({
                        title: 'Add Facebook Account',
                        html: '<div class="form-group">' +
                            '<label>Username <label>'+
                                  '<input id="id_username" type="text" name="username" class="form-control" />' +
                              '</div>'+
                             '<div class="form-group">' +
                            '<label>Password <label>'+
                                  '<input id="id_password" type="password" name="password" class="form-control" />' +
                              '</div>' ,
                        showCancelButton: true,
                        confirmButtonClass: 'btn btn-success btn-fill',
                        cancelButtonClass: 'btn btn-danger btn-fill',
                        buttonsStyling: false
                    }).then(function(result) {
                        username = $("#id_username").val();
                        password = $("#id_password").val();
                        save_new_account(username, password, new_account_callback);
                    }).catch(swal.noop)
            }
    } // end show_swal

    } // end of app.





});
