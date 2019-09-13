from django.conf.urls import include, url
from booktest import views

urlpatterns = [
    url(r'^index$', views.index), # 图书信息页面
    url(r'^create$', views.create),
]
