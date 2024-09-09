document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById('loginBtn');
    const loginPopup = document.getElementById('myModal');
    const closeBtn = document.getElementById('close');

    loginBtn.addEventListener('click', function() {
        loginPopup.style.display = "block";
    });

    closeBtn.addEventListener('click', function() {
        loginPopup.style.display = "none"; // 隐藏弹窗
    });
});

$(document).ready(function () {
       $('#loginForm').on('click', function (e) {
           e.preventDefault(); // 阻止默认的表单提交行为

           // 获取输入的值
           const dbAccountInput = $('input[name="db_account"]').val();

           // 发起AJAX请求
           $.ajax({
               type: 'POST',
               url: '/mysql',
               data: $(this).closest('form').serialize(),
               dataType: 'json',
               success: function (response) {
                   const data = response.data;
                   if (data.success) {
                       console.log("登录成功");

                       // 将用户名保存到localStorage
                       localStorage.setItem('loggedInUser', dbAccountInput);

                       // 重定向到主页
                       window.location.href = "/";
                   }
               },
               error: function (jqXHR, textStatus, errorThrown) {
                   try {
                       const errorData = JSON.parse(jqXHR.responseText);
                       const errorMessage = errorData.data["错误："] || '未知错误';
                       $("#errorMessage").text(errorMessage);
                       $("#errorMessageContainer").removeClass("d-none"); // 显示错误消息容器
                   } catch (err) {
                       console.error("解析错误消息时出错:", err);
                       $("#errorMessage").text("发生未知错误，请稍后重试。");
                       $("#errorMessageContainer").removeClass("d-none"); // 显示错误消息容器
                   }
               }
           });

       });
   });
      document.addEventListener('DOMContentLoaded', function () {
    const loggedInUser = localStorage.getItem('loggedInUser');

    if (loggedInUser) {
        // 用户已登录，更新导航条按钮为“退出”并绑定登出逻辑
        $('#loginBtn')
            .text('退出')
            .off('click') // 移除原有点击事件
            .on('click', function () {
                localStorage.removeItem('loggedInUser');
                window.location.href = "/"; // 跳转到登录页面
            });
    } else {
        // 用户未登录，恢复导航条登录按钮原状
        $('#loginBtn').text('登录');
    }
});