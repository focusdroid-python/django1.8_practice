from django.conf.urls import url
from booktest import views

urlpatterns = [
    url(r'^index1$', views.index, name='index'),
    url(r'^temp_var$', views.temp_var),
    url(r'^login$', views.login),  # 显示登录页面
    url(r'^login_check$', views.login_check),
    url(r'^change_pwd$', views.change_pwd), # 修改密码页面
    url(r'^change_pwd_action$', views.change_pwd_action),
    url(r'^verify_code$', views.verify_code), # 验证码
    url(r'^url_reverse$', views.url_reverse), # 反向解析
    url(r'^test_redirect$', views.test_redirect),
]
