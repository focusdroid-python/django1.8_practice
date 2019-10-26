from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import re
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from user.models import User
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
    print(data)
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

    # 返回应答
    response = {"status": "success", "msg": "注册成功"}
    return JsonResponse(response)
    # return redirect(reverse('goods:index')) # 前后端未分离写法