from django.conf.urls import url
from user import views
# from user.views import RegisterView

urlpatterns = {
    url(r'^register$', views.register, name='register'),  # 注册
    url(r'^register_handle$', views.register_handle, name='register_handle'),  # 注册处理
    # url(r'^register$', RegisterView.as_view(), name='register'),  # 类视图, 用于前后端未分离
    url(r'^active/(?P<token>.*)$', views.active, name='active'), # 用户激活
    url(r'^login$', views.login, name='login'),
}
