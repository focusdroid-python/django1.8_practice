from django.conf.urls import include, url
from booktest import views

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^showarg(\d+)$', views.showarg), # 捕获url参数
    url(r'^showtwo(?P<num>\d+)$', views.showtwo),
    url(r'^login$', views.login), # 显示登录页面
    url(r'^login_check$', views.login_check),
    url(r'^ajax_test$', views.ajax_test), # 显示ajax页面
    url(r'^ajax_handle$', views.ajax_handle), # ajax请求
    url(r'^login_ajax$', views.login_ajax), # 显示ajax登录页面
    url(r'^login_ajax_hangle$', views.login_ajax_hangle), # ajax提交地址
    url(r'^set_cookie$', views.set_cookie),
    url(r'^get_cookie$', views.get_cookie),
    url(r'^set_session', views.set_session),
    url(r'^get_session$', views.get_session),
]