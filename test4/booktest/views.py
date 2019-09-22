from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse
from booktest.models import BookInfo

from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO
import random

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

    # 获取验证码
    code = request.POST.get('code')
    verifycode = request.session.get('verifycode')
    # 进行验证码校验
    if code != verifycode:
        return redirect('/login')
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

def verify_code(request):
    '''随机验证码'''
    # 1.创建画面对象
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (255, 255, 255)
    width = 200
    height = 45

    im = Image.new('RGB', (width, height), bgcolor)
    # 2.创建画笔对象
    draw = ImageDraw.Draw(im)
    # 3.调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 调用画笔的point()函数绘制6条干扰线
    for i in range(6):
        x1 = int(random.randrange(0, width))
        y1 = int(random.randrange(0, height))
        x2 = int(random.randrange(0, width))
        y2 = int(random.randrange(0, height))
        fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        draw.line([(x1, y1), (x2, y2)], fill=fill, width=2)

    # 4.定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456klmnopqrstuvwsyzLMNOPQRS789TUVWXYZ0abcdefghij'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    # 构造字体类型和大小
    font = ImageFont.truetype('FreeMono.ttf', random.randrange(23, 40))
    # 绘制4个字
    draw.text((15, 10), rand_str[0], font=font, fill=random.randrange(0, 255))
    draw.text((65, 10), rand_str[1], font=font, fill=random.randrange(0, 255))
    draw.text((120, 10), rand_str[2], font=font, fill=random.randrange(0, 255))
    draw.text((175, 10), rand_str[3], font=font, fill=random.randrange(0, 255))
    # 5.释放画笔
    del draw
    # 6.存入session，用于做进一步验证
    request.session['verifycode'] = rand_str

    # 内存文件操作(python2)
    # import cStringIO
    # buf = cStringIO.StringIO()

    # 内存文件操作(python3)
    from io import BytesIO
    buf = BytesIO()
    print(buf)
    # 7.将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 8.将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def url_reverse(request):
    '''url反向解析'''
    return render(request, 'booktest/url_reverse.html')

from django.core.urlresolvers import reverse
# urlresolvers 重定向
def test_redirect(request):
    # 重定向到/index
    # url = reverse('booktest:index')
    # 普通参数： /show_args/1/2
    # url = reverse('booktest:show_args', args=(1,2))
    # 关键字参数
    url = reverse('booktest:show_kwargs', kwargs={'c': 3, 'd': 4})
    return redirect(url)





