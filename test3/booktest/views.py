from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import timedelta, datetime
# Create your views here.
def index(request):
    '''首页'''
    return render(request, 'booktest/index.html')


def showarg(request, num):
    return HttpResponse(num)

def showtwo(request, num):
    return HttpResponse(num)

def login(request):
    '''显示登陆页面'''
    # 获取cookie的username
    if 'username' in request.COOKIES and 'password' in request.COOKIES:
        # 获取cookie中的用户名
        username = request.COOKIES['username']
        password = request.COOKIES['password']
        return redirect('/index')
    else:
        username = ''
        password = ''
    return render(request, 'booktest/login.html', {'username': username, 'password': password})

def login_check(request):
    '''登录校验视图'''
    ## request.POST 保存的是post方式提交的参数
    ## request.GET 保存的是get方式提交的参数
    # request.method请求方式
    # print(request.method)
    # request.path 只显示路由地址，不显示参数和域名
    # print(request.path)
    # 1. 获取用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember') # 记住用户名的复选框
    # 2. 进行登录校验
    # 实际的情况：根据用户名和密码查找数据库
    # 模拟: tree   111
    if username == 'tree' and password == '111':
        response = redirect('/index') # 返回值就是HttpResponse
        if remember == 'on':
            response.set_cookie('username', username, max_age=2*24*3600)
            response.set_cookie('password', password, max_age=2*24*3600)
            return response
    else:
        return redirect('/login')

    # 3. 返回应答
    return HttpResponse('ok')

# /testajax
def ajax_test(request):
    '''显示ajax页面'''
    return render(request, 'booktest/ajaxtest.html')

def ajax_handle(request):
    '''ajax处理'''
    return JsonResponse({'res': 200})

def login_ajax(request):
    '''ajax请求的页面'''
    return render(request, 'booktest/login_ajax.html')

def login_ajax_hangle(request): # ajax登录校验
    name = request.POST.get('username')
    pwd = request.POST.get('password')
    if name == 'tree' and pwd == '1':
        return JsonResponse({'res': 200})
    else :
        return redirect('/login_ajax')


def set_cookie(request):
    '''设置cookie信息'''
    response = HttpResponse('设置cookie')
    response.set_cookie('num', 1, max_age=14*24*3600)
    # response.set_cookie('num', 1, expires=datetime.now()+timedelta(day=14))
    return response

def get_cookie(request):
    '''获取cookie'''
    num = request.COOKIES['num']
    return  HttpResponse(num)

def set_session(request):
    '''设置session'''
    request.session['username'] = 'focusdroid'
    request.session['age'] = 25
    return HttpResponse('设置session成功')

def get_session(request):
    '''获取session'''
    username = request.session['username']
    age = request.session['age']
    return HttpResponse(username+'---'+age)










