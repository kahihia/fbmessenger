$( document  ).ready(function() {



    function check_progress(){
        $.getJSON("/ajax/progress/", function(response){
            check_messenger = $.isEmptyObject(response.messenger);
            check_collector = $.isEmptyObject(response.collector);
            client_status = response.client;
            user_type = response.user_type;
            fb_account_status = response.fb_account_status;
            delta_time = response.delta_time;

            $(".wait_time_note").html("");
            $(".fb_account_status").html("");

            if(fb_account_status == -1) {
                $(".fb_account_status").html("Invalid Facebook Account!");
            } 
            else if(fb_account_status == 0) {
                wait_time = 24 - parseInt(delta_time);
                if (wait_time > 0) {
                    $(".wait_time_note").html("*Account is not available now. You have to wait for " + wait_time +" hours.*");
                }
            }
            
            $(".user_type").html(user_type);

            if(user_type != "")
                $(".collector_notification").hide();
            else
                $(".collector_notification").show();

            client_front = $("#client_status");
            if (client_status == true){
                client_front.html("Online");
            }else{
                client_front.html("Offline");
            }

            html_string = '';
            obj_count = 0;
            if (check_messenger == false ){
                $.each(response.messenger, function(index, value){
                    html_string += '<li><a href="#task'+ value.id +'">'+
                        '<i class="fa fa-spinner fa-spin"></i>'+
                        ' '+ value.name + '. Sent ' + value.sent + ' out of ' + value.total +'. '+
                        '</a></li>';
                    obj_count += 1;
                });
            }else{
            }

            if(check_collector == false){
                $.each(response.collector, function(index, value){
                    html_string += '<li><a href="#task'+ value.id +'">'+
                        '<i class="fa fa-spinner fa-spin"></i>'+
                        ' '+ value.name + '. Collected ' + value.collected + '</a></li>';
                    obj_count += 1;
                });

            }

            if (check_messenger == true && check_collector == true){
                html_string += '<li><a href="#done">'+
                    '<i class="fa fa-check"></i>'+
                    ' No running tasks.</a></li>';
            }

            var progress = $("#id_task_menu");
            var task_count = $("#task_count");
            progress.html(html_string);
            task_count.html(obj_count);

        });
    }
    progress_interval = setInterval(check_progress, 1000);

    function  send_message_callback(response){
        if (response === true){

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


    function  collect_end_callback(response){
        if (response === true){

            title = 'Collect!'
            type = 'success',
            text = 'Collecting done...'
        } else {
            title = 'Not deleted!'
            type = 'warning',
            text = 'Your account adcould not been deleted.'

        }
        clearInterval(collector_interval);

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

    function  collector_callback(response){

                title = 'Collecting...'
                type = 'info',
            // text = 'Messages are sending...'
                    html =
                        '<p><i class="fa fa-spinner fa-spin" style="font-size:60px"></i> </p>' +
                        '<p>Now we are collecting...' +
                        '<p>Collected profiles <b id="id_collect_count">0</b></p>';

                  swal({
                    title: title,
                    // text: text,
                    html: html,
                    // type: type,
                    showCancelButton: false,
                    showConfirmButton: true,
                    allowOutsideClick: true,
                    confirmButtonClass: 'btn btn-success btn-fill',
                    buttonsStyling: false,
                    confirmButtonText: 'Minimize',

                    }).then(function(result){
                      location.reload();
                  })
    }

    function  sending_message_callback(response){

                title = 'Sending...'
                type = 'info',
            // text = 'Messages are sending...'
                    html =
                        '<p><i class="fa fa-spinner fa-spin" style="font-size:60px"></i> </p>' +
                        '<p>Message is sending...' +
                        '<p>Sent <b id="id_count">0</b> out of <b id="id_total">'+ $("#id_recipients :selected").length +'</b><p>';

                  swal({
                    title: title,
                    // text: text,
                    html: html,
                    // type: type,
                    showCancelButton: false,
                    showConfirmButton: true,
                    allowOutsideClick: true,
                    confirmButtonClass: 'btn btn-success btn-fill',
                    buttonsStyling: false,
                    confirmButtonText: 'Minimize',

                    }).then(function(result){
                      location.reload();
                  })
    }


    function check_collect_status(){
        $.getJSON("/ajax/collect/last/", function(response){
            $("#id_collect_count").html(response.collected);
            if(response.done == true){
                     collect_end_callback(true);
             }
        });
    }

    function check_sent_status(){
        $.getJSON("/ajax/progress/last/", function(response){
            $("#id_count").html(response.sent);
            $("#id_total").html(response.total);
            if(response.sent == response.total){
                    send_message_callback(true);
            }
        });
    }

    // function send_message(before_callback, success_callback){
    function send_message(success_callback){
            $.ajax({
                url: "/create/messenger/",
                method: "POST",
                data: $("#id_messenger_form").serialize(),
                dataType: "json",
                // beforeSend: before_callback,
                success: success_callback

            });
    }


    function collector(success_callback){
            $.ajax({
                url: "/task/collector/",
                method: "POST",
                data: $("#id_collector_form").serialize(),
                dataType: "json",
                // beforeSend: before_callback,
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

    function  user_edit_callback(response){
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
                            $users_table.bootstrapTable('refresh');
                        })
    }

    function user_edit(data, callback){

            $.ajax({
                url: "/ajax/users/edit/",
                method: "POST",
                data: data,
                dataType: "json",
                success: callback
            });
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

    function  remove_user_callback(response){
        if (response.success === true){

            title = 'Deleted!'
            type = 'success',
            text = 'User  has been deleted.'
        } else {
            title = 'Not deleted!'
            type = 'warning',
            text = 'User could not been deleted.'

        }
                              swal({
                                title: title,
                                text: text,
                                type: type,
                                confirmButtonClass: "btn btn-success btn-fill",
                                buttonsStyling: false
                                }).then(function(result){
                                  $users_table.bootstrapTable('refresh');
                              })
    }


    function remove_user(id, callback){
        if (id){
            $.ajax({
                url: "/ajax/users/remove/",
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
                            }).catch(swal.noop);
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
                            }).catch(swal.noop);

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

                                   // send_message(sending_message_callback, send_message_callback);
                                   send_message(sending_message_callback);
                                   check_interval = setInterval(check_sent_status, 1000);
                                   progress_interval = setInterval(check_progress, 1000);

                            }).catch(swal.noop);
                }

            } else if(type == "collector"){
                if ($("#id_collector_form").valid()){
                        swal({
                                title: 'Are you sure?',
                                text: 'This will run Facebook profile collector!',
                                type: 'warning',
                                showCancelButton: true,
                                confirmButtonText: 'Yes, collect!',
                                cancelButtonText: 'No',
                                confirmButtonClass: "btn btn-success btn-fill",
                                cancelButtonClass: "btn btn-danger btn-fill",
                                buttonsStyling: false
                            }).then(function(result) {

                                   collector(collector_callback);
                                   collector_interval = setInterval(check_collect_status, 1000);
                                   progress_interval = setInterval(check_progress, 1000);

                            }).catch(swal.noop);

                }

            } else if(type == "remove-user"){
                        swal({
                                title: 'Are you sure?',
                                text: 'User will be removed!',
                                type: 'warning',
                                showCancelButton: true,
                                confirmButtonText: 'Yes, remove it!',
                                cancelButtonText: 'No, keep it',
                                confirmButtonClass: "btn btn-success btn-fill",
                                cancelButtonClass: "btn btn-danger btn-fill",
                                buttonsStyling: false
                            }).then(function(result) {

                                   remove_user(data, remove_user_callback);
                            }).catch(swal.noop);
            } else if(type == "edit-user"){
                swal({
                        title: 'Edit User',
                        html: '<form id="id_user_edit_form" action="" method="POST">'+
                            '<div class="form-group">' +
                            '<label>Username <label>'+
                                  '<input id="id_id" value="'+ data.id +'" type="text" name="id" class="form-control hidden" />' +
                                  '<input id="id_username" value="'+ data.username +'" type="text" name="username" class="form-control" required/>' +
                              '</div>'+
                              '<div class="form-group">'+
                            '<label>First name <label>'+
                                  '<input id="id_first_name" value="'+ data.firstname +'" type="text" name="first_name" class="form-control" />' +
                              '</div>'+
                              '<div class="form-group">'+
                            '<label>Last name <label>'+
                                  '<input id="id_last_name" value="'+ data.lastname +'" type="text" name="last_name" class="form-control" />' +
                              '</div>'+
                              '<div class="form-group">'+
                            '<label>   E-mail <label>'+
                                  '<input id="id_email" value="'+ data.email +'" type="text" name="email" class="form-control" required/>' +
                              '</div>'+
                             '<div class="form-group">' +
                            '<label>Password <label>'+
                                  '<input id="id_edit_password" type="password" name="password" class="form-control" />' +
                              '</div></form>' ,
                        showCancelButton: true,
                        confirmButtonClass: 'btn btn-success btn-fill',
                        cancelButtonClass: 'btn btn-danger btn-fill',
                        buttonsStyling: false
                    }).then(function(result) {
                        //id_messenger_form
                        var data = $("#id_user_edit_form").serialize();
                        data = data + '&csrfmiddlewaretoken=' + $("input[name=csrfmiddlewaretoken]").val();
                        user_edit(data, user_edit_callback);
                    }).catch(swal.noop)
            }// end if
    } // end show_swal

    } // end of app.




// tables
        window.operateEvents = {
            'click .edit': function (e, value, row, index) {
                window.location.replace("/update/fburl/"+ row.id +"")
            },
            'click .remove': function (e, value, row, index) {
                app.show_swal('remove-url', row.id);
                // $table.bootstrapTable('remove', {
                //     field: 'id',
                //     values: [row.id]
                // });
            }
        };

        window.userEvents = {
            'click .edit': function (e, value, row, index) {
                app.show_swal('edit-user', row);
            },
            'click .remove': function (e, value, row, index) {
                app.show_swal('remove-user', row.id);
            }
        };
    });
    
    
    function imageFormatter(value, row, index){
        if(row.image_path != "") 
            return '<img class="profile-image" src="' + row.image_path +'"></div>'
    }

    function dateAddFormatter(value, row, index){
        if(row.date_to_be_added != "") {
            date_list = row.date_to_be_added.split("-")
            return date_list[2] + "/" + date_list[1] + "/" + date_list[0]
        }
    }

    function messagedFormatter(value, row, index){
        if(row.is_messaged == true){
            mark = '<div class=""><i style="color:green" class="fa fa-check-square"></i></div>'
        }else{

            mark = '<div class=""> <i class="fa fa-square-o"></i></div>'
        }
        return mark

    }

    function historyFormatter(value, row, index){
        if(row.done == true){
            mark = '<div class=""><i style="color:green" class="fa fa-check-square"></i></div>'
        }else{

            mark = '<div class=""> <i class="fa fa-spinner fa-spin"></i></div>'
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
    var $messenger_history = $('#messenger-history');
    var $collector_history = $('#collector-history');
    var $users_table = $('#users-table');

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

        $messenger_history.bootstrapTable({
            toolbar: ".toolbar",
            clickToSelect: true,
            showRefresh: true,
            search: true,
            showToggle: true,
            showColumns: true,
            pagination: true,
            sortOrder: 'desc',
            pageSize: 10,
            url: '/ajax/history/messenger/',
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


        $collector_history.bootstrapTable({
            toolbar: ".toolbar",
            clickToSelect: true,
            showRefresh: true,
            search: true,
            showToggle: true,
            showColumns: true,
            pagination: true,
            sortOrder: 'desc',
            pageSize: 10,
            url: '/ajax/history/collector/',
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

        $users_table.bootstrapTable({
            toolbar: ".toolbar",
            clickToSelect: true,
            showRefresh: true,
            search: true,
            showToggle: true,
            showColumns: true,
            pagination: true,
            sortOrder: 'desc',
            pageSize: 10,
            url: '/ajax/users/',
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
            $messenger_history.bootstrapTable('resetView');
            $collector_history.bootstrapTable('resetView');
            $users_table.bootstrapTable('resetView');
        });




});
