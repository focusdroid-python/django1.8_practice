# 使用selery
from django.conf import settings
from django.core.mail import send_mail
from celery import Celery

# 在人物处理者加这几行代码
# 防止calery在只用时候报错，需要进行一些初始化数据
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()

# 创建一个Celery的实例对象
app = Celery('celery_tasks.tasks', broker='redis://192.168.1.104:6379/8') # 写tasks文件的路径


# 定义任务函数
# 给下面的加一些信息
@app.task
def send_register_active_email(to_email, username, token):
    '''发送激活邮件'''
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [to_email]  # 收件人
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的帐户<br/><a href="http://192.168.1.108:8000/user/active/%s">http://192.168.1.108:8000/user/active/%s</a>' % (
    username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)  # 发送带有html标签的内容时候需要使用html_message这个字段
    # time.slepp(5)