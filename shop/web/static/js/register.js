$(document).on('submit','#register-form', function(e){
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/create/",
        data: {
            username: $(this).find('#username').val(),
            email: $(this).find('#email').val(),
            password: $(this).find('#password').val(),
            confirm_password: $(this).find('#confirm_password').val(),
            csrfmiddlewaretoken: $(this).find('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data){
            // console.log(response)
            alert(data);
        },
        error: (error) => {
            console.log(JSON.stringify(error));
        },
    });
});