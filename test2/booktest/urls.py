from django.conf.urls import include, url
from booktest import views

urlpatterns = [
    url(r'^index$', views.index), # 图书信息页面
    url(r'^create$', views.create), # 新增图书信息
    url(r'^delete(\d+)$', views.delete), # 删除点击图书
]
