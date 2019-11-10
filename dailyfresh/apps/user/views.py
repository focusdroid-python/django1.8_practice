from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse # 处理前后端未分离的跳转
from django.views.decorators.csrf import csrf_exempt  # 处理csrf报错 @csrf_exempt
from django.http import HttpResponse, JsonResponse  # 处理返回数据
from django.core.mail import send_mail
from django.conf import settings  # 使用其中 SECRET_KEY 作为密钥  使用其中的send_mail配置
from django.contrib.auth import authenticate, login, logout
from utils.mixin import LoginRequiredMixin

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from user.models import User, Address
from goods.models import GoodsSKU
import re
import json
from celery_tasks.tasks import send_register_active_email
from django.views.generic import View
from django_redis import get_redis_connection

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
    user.is_active = 0  # 设置账户未激活，默认是已激活
    user.save()

    # 发送激活邮件，包含激活链接,并且要把身份信息加密
    # 加密用户身份信息,生成激活的token
    serializer = Serializer(settings.SECRET_KEY, 3600)
    info = {'confirm': user.id}
    token = serializer.dumps(info)  # bytes
    token = token.decode('utf8')  # 解码

    # 发送邮件
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [mail]  # 收件人
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的帐户<br/><a href="http://192.168.1.108:8000/user/active/%s">http://192.168.1.108:8000/user/active/%s</a>' % (
    username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)  # 发送带有html标签的内容时候需要使用html_message这个字段
    # 异步celery有点问题,启动需要在目标机器启动使用
    # send_register_active_email.delay(mail, username, token) # delay()是经过@app.task函数装饰以后才有的函数

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


# def login(request):
#     '''显示登录页面'''
#     return render(request, 'login.html')


# 前后端未分离写法
class LoginView(View):
    '''登录的类视图'''

    def get(self, request):
        '''显示登录页面'''
        return render(request, 'login.html')

    @csrf_exempt
    def post(self, request):
        '''登录校验'''
        # 接受数据
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('passwd')
        rempasswd = data.get('rempasswd')
        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})
        # 业务处理，登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                # 记录用户的状态
                login(request, user)

                response = redirect(reverse('goods:index'))
                # 判断是否需要记住用户名
                print(rempasswd)
                print(rempasswd == True)
                if rempasswd == True:
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                # return redirect('user:user')
                return JsonResponse({"status": "success", "msg": "登陆成功"}
)
            else:
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名密码错误
            return render(request, 'login.html', {'errmsg':'用户名密码错误'})


        # 返回应答

# 前后端分写法
# class LoginView(View):
#     '''登录的类视图'''
#
#     def get(self, request):
#         '''显示登录页面'''
#         if 'username' in request.COOKIES: #根据cooki自动填充
#             username = request.COOKIES.get('username')
#             print(username)
#         else:
#             username = ''
#             return render(request, 'login.html')
#
#     @csrf_exempt
#     def post(self, request):
#         '''登录校验'''
#         # 接受数据
#         data = json.loads(request.body.decode())
#         username = data.get('username')
#         passwd = data.get('passwd')
#         rempasswd = data.get('rempasswd')
#         # 校验数据
#         if not all([username, passwd]):
#             result = {"status": "error", "msg": "请将用户名和密码填写完整"}
#             return JsonResponse(result)
#
#         # 业务处理
#         user = authenticate(username=username, password=passwd) # redis记住登录状态
#         if user is not None:
#             # 用户名密码正确
#             if user.is_active:
#                 # 用户已激活
#                 # 使用redis记住用户登录状态
#                 print(user)
#                 # login(request, user) # redis连接还有点问题
#                 # next_url = request.GET.get('next', reverse('goods:index'))
#                 # response = redirect(next_url)
#
#                 # 判断是否需要记住用户名
#                 response = HttpResponse() # 使用response设置cookie
#                 if rempasswd == True: # 前端做存储
#                     # 记住用户名
#                     response.set_cookie('username', username, max_age=7 * 24 * 3600)
#                 else:
#                     response.delete_cookie('username')
#
#                 success_active = {"status": "success", "msg": "登陆成功"}
#                 return JsonResponse(success_active)
#
#             else:
#                 # 用户未激活
#                 no_active = {"status": 'error', "msg": '请先激活账户'}
#                 return JsonResponse(no_active)
#         else:
#             # 用户名密码错误
#             err_user = {"status": 'error', "msg": '用户名或者密码错误'}
#             return JsonResponse(err_user)
#
#
#         # 返回应答

# /user/logout
class LogoutView(View):
    '''退出登录'''
    def get(self, request):
        logout(request)
        # 用户退出之后，跳转到首页
        return redirect(reversed('goods:index'))

# 登录判断是否在有效期
# # /user
# class UserInfoView(LoginRequiredMixin, View):
#     '''用户中心-信息页'''
#     def get(self, request):
#         '''显示'''
#         return render(request, 'user_center_info.html')
# # /user/order
# class UserOrderView(LoginRequiredMixin, View):
#     '''用户中心-订单页面'''
#     def get(self, request):
#         '''显示订单页面'''
#         return render(request, 'user_center_order.html')
# # /user/address
# class AddressView(LoginRequiredMixin, View):
#     '''地址信息页'''
#     def get(self, request):
#         '''显示地址页面'''
#         return render(request, 'user_center_address.html')
# /user
class UserInfoView(View):
    '''用户中心-信息页'''
    def get(self, request):
        '''显示'''
        # request.user.is_authenticated()
        # django会给request对象添加一个属性request.user
        # 用户未登录->user是AnonymouseUser类的一个实例
        # 用户登录->user是user类的一个实例
        # request.user.is_authenticated()

        # 获取用户的个人信息
        user = request.user
        address = Address.objects.get_default_address(user)

        # 获取用户的浏览记录
        # from redis import StrictRedis #
        # sr = StrictRedis(host='192.168.1.104', port='6379', db='9')
        con = get_redis_connection('default')
        history_key = 'history_%d'%user.id

        # 获取用户最新的浏览的5个商品的id
        sku_ids = con.lrange(history_key, 0, 4)

        # 从数据库查询商品浏览的具体信息
        # goods_li = GoodsSKU.objects.filter(id__in=sku_ids)
        #
        # goods_res = []
        # for a_id in sku_ids:
        #     for goods in goods_li:
        #         if a_id == goods.id:
        #             goods_res.append(goods)
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)

        # 组织上写文
        context = {'page':'user', 'address': address, 'goods_li':goods_li}

        # 处理你本身给模板文件传递的变量之外，django会把request.user自动传递给用户
        # print(request.user)
        # print(request.user.is_authenticated)
        return render(request, 'user.html', context)

# /user/order
class UserOrderView(View):
    '''用户中心-订单页面'''
    def get(self, request):
        '''显示订单页面'''
        return render(request, 'order.html')

# /user/address
class AddressView(LoginRequiredMixin, View):
    '''地址信息页'''
    def get(self, request):
        '''显示地址页面'''
        user = request.user
        address = Address.objects.get_default_address(user)
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在默认收货地址
        #     address = None
        return render(request, 'address.html', {'page':'address', 'address':address})

    def post(self, request):
        '''添加地址'''
        # 接受地址
        data = json.loads(request.body.decode())
        name = data.get('name')
        addr = data.get('addr')
        zipCode = data.get('zipCode')
        phone = data.get('phone')

        if not all([name, addr, phone]):
            return render(request, 'address.html', {'errmsg':'数据不完整'})

        # 校验数据
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}', phone):
            return render(request, 'address.html', {'errmeg':'手机号码不符合规范'})
        # 业务处理：地址添加
        # 获取登录用户对应的User对象
        user = request.user

        address = Address.objects.get_default_address(user)
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     # 不存在默认收货地址
        #     address = None

        if address:
            is_default = False
        else:
            is_default = True

        # 添加数据
        Address.objects.create(user=user, receiver=name, addr=addr, zip_code=zipCode, phone=phone, is_default=is_default)

        # 返回应答,刷新页面
        return redirect(reverse('user:address'))


















