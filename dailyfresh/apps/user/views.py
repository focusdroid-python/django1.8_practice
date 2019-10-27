from django.shortcuts import render, redirect
# from django.core.urlresolvers import reverse # 处理前后端未分离的跳转
from django.views.decorators.csrf import csrf_exempt # 处理csrf报错 @csrf_exempt
from django.http import HttpResponse, JsonResponse # 处理返回数据
from django.core.mail import send_mail
from django.conf import settings # 使用其中 SECRET_KEY 作为密钥  使用其中的send_mail配置

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from user.models import User
import re
import json
from celery_tasks.tasks import send_register_active_email
# from django.views.generic import View

# Create your views here.

# /user/register
def register(request):
    '''显示注册页面'''
    return render(request, 'register.html')

# 解除django框架csrf限制
@csrf_exempt
def register_handle(request):
    '''进行注册处理'''
    # 接受数据(下面是通过表单接受的)
    # username = request.POST.get('username')
    # passwd = request.POST.get('passwd')
    # mail = request.POST.get('mail')
    # single = request.POST.get('single')
    # 通过axios提交通过request.body提交的经过转换得到的数据
    # data_byte = request.body
    # data_str = data_byte.decode()
    # data_json = json.loads(data_str)
    data = json.loads(request.body.decode())
    print(request.method)
    username = data.get('username')
    passwd = data.get('passwd')
    mail = data.get('mail')
    single = data.get('single')

    # 进行数据校验
    if not all([username, passwd, mail]):
        # 数据不完整
        # return render(request, 'register.html', {'errmsg':'数据不完整'})
        result = {"status": "error", "msg": "请将数据填写完整"}
        return JsonResponse(result)
    # 校验邮箱
    if not re.match(r'[a-zA-Z0-9][\w\.\-]*@[a-zA-Z0-9\-]+(\.[a-z]{2,5}){1,2}$', mail):
        # return render(request, 'register.html', {'msg': '邮箱不合法'})
        mailresult = {"status": "error", "msg": "邮箱不合法"}
        return JsonResponse(mailresult)
    # 判断勾选
    if single != True:
        singleresult = {"status": "error", "msg": "请勾选协议"}
        return JsonResponse(singleresult)
        # return render(request, 'register.html', {'msg': '请勾选协议'})
    # 校验用户名是否重复
    try:
        is_dou_user = User.objects.get(username=username)
    except User.DoesNotExist:
        # 用户名不存在
        is_dou_user = None

    if is_dou_user:
        is_dou_userresult = {"status": "error", "msg": "用户名已经存在，请重新输入一个用户名"}
        return JsonResponse(is_dou_userresult)

    # 进行业务处理：进行用户注册
    # user = User()
    # user.username = username
    # user.passwd = passwd
    # user.mail = mail
    # user.single = single
    # user.save()
    user = User.objects.create_user(username, mail, passwd)
    user.is_active = 0 # 设置账户未激活，默认是已激活
    user.save()

    # 发送激活邮件，包含激活链接,并且要把身份信息加密
    # 加密用户身份信息,生成激活的token
    serializer = Serializer(settings.SECRET_KEY, 3600)
    info = {'confirm': user.id}
    token = serializer.dumps(info) # bytes
    token = token.decode('utf8') # 解码

    # 发送邮件
    # subject = '天天生鲜欢迎信息'
    # message = ''
    # sender = settings.EMAIL_FROM # 发件人
    # receiver = [mail] # 收件人
    # html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的帐户<br/><a href="http://192.168.1.108:8000/user/active/%s">http://192.168.1.108:8000/user/active/%s</a>'%(username, token, token)
    # send_mail(subject, message, sender, receiver, html_message=html_message) # 发送带有html标签的内容时候需要使用html_message这个字段
    send_register_active_email.delay(mail, username, token) # delay()是经过@app.task函数装饰以后才有的函数


    # 返回应答
    response = {"status": "success", "msg": "注册成功"}
    return JsonResponse(response)
    # return redirect(reverse('goods:index')) # 前后端未分离写法


# class RegisterView(View): # 适合前后端未分离，建议不要用
#     '''注册'''
#     def get(self, request):
#         '''显示注册页面'''
#         return render(request, 'register.html')
#     def post(self, request):
#         '''进行注册处理'''
#         data = json.loads(request.body.decode())
#         print(request.method)
#         username = data.get('username')
#         passwd = data.get('passwd')
#         mail = data.get('mail')
#         single = data.get('single')
#
#         # 进行数据校验
#         if not all([username, passwd, mail]):
#             # 数据不完整
#             # return render(request, 'register.html', {'errmsg':'数据不完整'})
#             result = {"status": "error", "msg": "请将数据填写完整"}
#             return JsonResponse(result)
#         # 校验邮箱
#         if not re.match(r'[a-zA-Z0-9][\w\.\-]*@[a-zA-Z0-9\-]+(\.[a-z]{2,5}){1,2}$', mail):
#             # return render(request, 'register.html', {'msg': '邮箱不合法'})
#             mailresult = {"status": "error", "msg": "邮箱不合法"}
#             return JsonResponse(mailresult)
#         # 判断勾选
#         if single != True:
#             singleresult = {"status": "error", "msg": "请勾选协议"}
#             return JsonResponse(singleresult)
#             # return render(request, 'register.html', {'msg': '请勾选协议'})
#         # 校验用户名是否重复
#         try:
#             is_dou_user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             # 用户名不存在
#             is_dou_user = None
#
#         if is_dou_user:
#             is_dou_userresult = {"status": "error", "msg": "用户名已经存在，请重新输入一个用户名"}
#             return JsonResponse(is_dou_userresult)
#
#         # 进行业务处理：进行用户注册
#         # user = User()
#         # user.username = username
#         # user.passwd = passwd
#         # user.mail = mail
#         # user.single = single
#         # user.save()
#         user = User.objects.create_user(username, mail, passwd)
#         user.is_active = 0  # 设置账户未激活，默认是已激活
#         user.save()
#
#         # 返回应答
#         response = {"status": "success", "msg": "注册成功"}
#         return JsonResponse(response)
#         # return redirect(reverse('goods:index')) # 前后端未分离写法

def active(request, token):
    '''用户激活链接'''
    # 进行解密， 获取需要激活的信息
    serializer = Serializer(settings.SECRET_KEY, 3600)

    try:
        info = serializer.loads(token)
        # 获取待激活用户id
        user_id = info['confirm']
        # 根据id获取用户信息
        user = User.objects.get(id=user_id)
        user.is_active = 1
        user.save()

        # 激活之后的跳转(应该直接提示激活成功)
        # activeresult = {"status": "success", "msg": "激活成功"}
        # return JsonResponse(activeresult)
        return HttpResponse('邮箱激活成功')

    except SignatureExpired as e:
        # 激活链接已过期
        expireToken = {"status": "error", "msg": "激活链接已过期"}
        return JsonResponse(expireToken)

def login(request):
    '''显示登录页面'''
    return render(request, 'login.html')

















