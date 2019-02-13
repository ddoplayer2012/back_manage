
function login(){
    /*
    * 登录函数
    * */
    var username = jQuery('input.form-control[type=text]').val();
    var password = jQuery('input.form-control[type=password]').val()
    jQuery.ajax({
        type: 'POST',
        url: '/login/login_check/',
        data: {'username': username, 'password': password},
        dataType: "json",
        success: function (response) {
            if(response.status=='ok'){
                // 登录成功
                window.location.href="/index";
            }else{
                jQuery("#login_result").text(response.error);
            }
        },
        error: function (xhr) {

        }
    });
}