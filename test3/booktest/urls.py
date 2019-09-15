from django.conf.urls import include, url
from booktest import views

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^showarg(\d+)$', views.showarg), # 捕获url参数
    url(r'^showtwo(?P<num>\d+)$', views.showtwo),
]