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

    function  edit_account_callback(response){
        if (response.success === true){

            type = 'success',
            html = 'Account edited successfully.'
        } else {
            type = 'warning',
            html = 'Could not edited account.'

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

    function edit_account(id, username, password, callback){

        if (username){
            $.ajax({
                url: "/ajax/edit/fbaccount/",
                method: "POST",
                data: {csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    id: id,
                    username: username,
                    password: password },
                success: callback

            });
        }
    }

    function  remove_account_callback(response){
        if (response.success === true){

            title = 'Deleted!'
            type = 'success',
            text = 'Your account has been deleted.'
        } else {
            title = 'Not deleted!'
            type = 'warning',
            text = 'Your account could not been deleted.'

        }
                              swal({
                                title: title,
                                text: text,
                                type: type,
                                confirmButtonClass: "btn btn-success btn-fill",
                                buttonsStyling: false
                                }).then(function(result){
                                  location.reload();
                              })

    }


    function remove_account(id, callback){
        console.log(id);
        if (id){
            $.ajax({
                url: "/ajax/remove/fbaccount/",
                method: "POST",
                data: {csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    id: id},
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
            } else if(type == "remove-account"){

                        swal({
                                title: 'Are you sure?',
                                text: 'You will not be able to recover this account!',
                                type: 'warning',
                                showCancelButton: true,
                                confirmButtonText: 'Yes, delete it!',
                                cancelButtonText: 'No, keep it',
                                confirmButtonClass: "btn btn-success btn-fill",
                                cancelButtonClass: "btn btn-danger btn-fill",
                                buttonsStyling: false
                            }).then(function() {

                                   remove_account(data, remove_account_callback);
                            });
            } else if(type == "edit-account"){
                a = $.getJSON("/ajax/get/fbaccount/"+ data +"/", function(result){
                    username = result.username;
                }).then(function(){
                swal({
                        title: 'Edit Facebook Account',
                        html: '<div class="form-group">' +
                            '<label>Username <label>'+
                                  '<input id="id_edit_username" value="'+ username +'" type="text" name="username" class="form-control" />' +
                              '</div>'+
                             '<div class="form-group">' +
                            '<label>Password <label>'+
                                  '<input id="id_edit_password" type="password" name="password" class="form-control" />' +
                              '</div>' ,
                        showCancelButton: true,
                        confirmButtonClass: 'btn btn-success btn-fill',
                        cancelButtonClass: 'btn btn-danger btn-fill',
                        buttonsStyling: false
                    }).then(function(result) {
                        username = $("#id_edit_username").val();
                        password = $("#id_edit_password").val();
                        edit_account(data, username, password, edit_account_callback);
                    }).catch(swal.noop)
                });
            } // end if
    } // end show_swal

    } // end of app.





});
