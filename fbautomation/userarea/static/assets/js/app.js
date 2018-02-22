$( document  ).ready(function() {

    function  send_message_callback(response){
        if (response.status === true){

            title = 'Sent!'
            type = 'success',
            text = 'Messages are sent...'
        } else {
            title = 'Not deleted!'
            type = 'warning',
            text = 'Your account adcould not been deleted.'

        }
        clearInterval(check_interval);

          swal({
            title: title,
            text: text,
            type: type,
            confirmButtonClass: "btn btn-success btn-fill",
            buttonsStyling: false
            }).then(function(result){
              window.location.replace("/facebookurls/");
          })
    }

    function  sending_message_callback(response){

                title = 'Sending...'
                type = 'info',
            // text = 'Messages are sending...'
                    html =
                        '<p><i class="fa fa-spinner fa-spin" style="font-size:60px"></i> </p>' +
                        '<p>Message is sending...' +
                        '<p>Sent <b id="id_count">0</b> out of '+ $("#id_recipients :selected").length +'<p>';
                  swal({
                    title: title,
                    // text: text,
                    html: html,
                    // type: type,
                    showCancelButton: false,
                    showConfirmButton: false,
                    allowOutsideClick: false

                    }).then(function(result){
                      location.reload();
                  })
    }

    function check_sent_status(){
        $.getJSON("/ajax/messaged/", function(response){
            $("#id_count").html(response.count);
        });
    }

    function send_message(before_callback, success_callback){
            $.ajax({
                url: "/create/messenger/",
                method: "POST",
                data: $("#id_messenger_form").serialize(),
                dataType: "json",
                beforeSend: before_callback,
                success: success_callback

            });
    }

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

    function  remove_url_callback(response){
        if (response.success === true){

            title = 'Deleted!'
            type = 'success',
            text = 'Your URL has been deleted.'
        } else {
            title = 'Not deleted!'
            type = 'warning',
            text = 'Your URL could not been deleted.'

        }
                              swal({
                                title: title,
                                text: text,
                                type: type,
                                confirmButtonClass: "btn btn-success btn-fill",
                                buttonsStyling: false
                                }).then(function(result){
                                  // location.reload();
                                  $table.bootstrapTable('refresh');
                              })
    }

    function remove_url(id, callback){
        if (id){
            $.ajax({
                url: "/ajax/remove/fburl/",
                method: "POST",
                data: {csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                    id: id},
                success: callback

            });
        }
    }

    function remove_account(id, callback){
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
                }).then(function(result){
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
            } else if(type == "remove-url"){
                        swal({
                                title: 'Are you sure?',
                                text: 'You will not be able to recover this URL!',
                                type: 'warning',
                                showCancelButton: true,
                                confirmButtonText: 'Yes, delete it!',
                                cancelButtonText: 'No, keep it',
                                confirmButtonClass: "btn btn-success btn-fill",
                                cancelButtonClass: "btn btn-danger btn-fill",
                                buttonsStyling: false
                            }).then(function(result) {

                                   remove_url(data, remove_url_callback);
                            });

            } else if(type == "messenger"){
                if ($("#id_messenger_form").valid()){
                        swal({
                                title: 'Are you sure?',
                                text: 'Message will be sent to recipients!',
                                type: 'warning',
                                showCancelButton: true,
                                confirmButtonText: 'Yes, send it!',
                                cancelButtonText: 'No',
                                confirmButtonClass: "btn btn-success btn-fill",
                                cancelButtonClass: "btn btn-danger btn-fill",
                                buttonsStyling: false
                            }).then(function(result) {

                                   send_message(sending_message_callback, send_message_callback);
                                   check_interval = setInterval(check_sent_status, 1000);

                            });
                }

            }// end if
    } // end show_swal

    } // end of app.




// tables
        window.operateEvents = {
            'click .edit': function (e, value, row, index) {
                window.location.replace("/update/fburl/"+ row.id +"")
            },
            'click .remove': function (e, value, row, index) {
                console.log(row.id);
                app.show_swal('remove-url', row.id);
                // $table.bootstrapTable('remove', {
                //     field: 'id',
                //     values: [row.id]
                // });
            }
        };
    });

function messagedFormatter(value, row, index){
    console.log(row);
    if(row.is_messaged == true){
        mark = '<div class=""><i style="color:green" class="fa fa-check-square"></i></div>'
    }else{

        mark = '<div class=""> <i class="fa fa-square-o"></i></div>'
    }
    return mark

}
    function operateFormatter(value, row, index) {
        return [
            '<a rel="tooltip" title="Edit" class="btn btn-simple btn-warning btn-icon table-action edit" href="javascript:void(0)">',
                '<i class="ti-pencil-alt"></i>',
            '</a>',
            '<a rel="tooltip" title="Remove" class="btn btn-simple btn-danger btn-icon table-action remove" href="javascript:void(0)">',
                '<i class="ti-close"></i>',
            '</a>'
        ].join('');
    }
    var $table = $('#bootstrap-table');

    $().ready(function(){
        $table.bootstrapTable({
            toolbar: ".toolbar",
            clickToSelect: true,
            showRefresh: true,
            search: true,
            showToggle: true,
            showColumns: true,
            pagination: true,
            sortOrder: 'desc',
            pageSize: 10,
            url: '/ajax/profile/',
            sidePagination: 'server',
            clickToSelect: false,
            pageList: [10,20,30,50,100],

            formatShowingRows: function(pageFrom, pageTo, totalRows){
                //do nothing here, we don't want to show the text "showing x of y from..."
            },
            formatRecordsPerPage: function(pageNumber){
                return pageNumber + " rows visible";
            },
            icons: {
                refresh: 'fa fa-refresh',
                toggle: 'fa fa-th-list',
                columns: 'fa fa-columns',
                detailOpen: 'fa fa-plus-circle',
                detailClose: 'fa fa-minus-circle'
            }
        });

        //activate the tooltips after the data table is initialized
        $('[rel="tooltip"]').tooltip();

        $(window).resize(function () {
            $table.bootstrapTable('resetView');
        });









});
