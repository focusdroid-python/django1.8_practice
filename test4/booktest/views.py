from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse
from booktest.models import BookInfo

# Create your views here.

def my_render(request, template_path, context={}):
    # 1。 加载模板文件，获取一个模板对象
    temp = loader.get_template(template_path)
    # 2. 定义模板上下文，给模板文件传数据
    context = RequestContext(request, {})
    # 3. 模板渲染，产生一个替换后的html内容
    res_html = temp.render(context)
    # 4. 返回应答
    return HttpResponse(res_html)

def index(request):
    return my_render(request, 'booktest/index.html')

def temp_var(request):
    '''模板变量'''
    my_dict = {'title': '字典键值'}
    my_list = [1,2,3]
    book = BookInfo.objects.get(id=1)
    context = {'my_dict': my_dict, 'my_list': my_list, 'book': book}
    return render(request, 'booktest/temp_var.html', context)

# 是否登录的装饰器
def login_require(view_func):
    '''登录判断装饰器'''
    def wrapper(request, *args, **view_Kwargs):
        # 判断用户是否登录
        if request.session.has_key('isLogin'):
            # 用户已登录，调用对应视图
            return view_func(request, *args, **view_Kwargs)
        else:
            # 用户未登录
            return redirect('/login')
    return wrapper

def login(request):
    '''显示登陆页面'''
    # 获取cookie的username
    if 'username' in request.COOKIES and 'password' in request.COOKIES:
        # 获取cookie中的用户名
        username = request.COOKIES['username']
        password = request.COOKIES['password']
        return redirect('/change_pwd')
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
        response = redirect('/change_pwd') # 返回值就是HttpResponse
        if remember == 'on':
            response.set_cookie('username', username, max_age=2*24*3600)
            response.set_cookie('password', password, max_age=2*24*3600)

            # 设置登录的标识
            request.session['isLogin'] = True
            request.session['username'] = username
            return response
    else:
        return redirect('/login')

    # 3. 返回应答
    return HttpResponse('ok')

@login_require
def change_pwd(request):
    '''显示修改密码页面'''
    return render(request, 'booktest/change_pwd.html')

def change_pwd_action(request):
    '''修改密码处理'''
    # 1。 获取新密码
    pwd = request.POST.get('pwd')
    # 获取用户名
    username = request.session['username']
    # 2. 实际开发中修改数据库内容

    # 3. 返回应答
    return HttpResponse('%s修改密码%s'% (username,pwd))




