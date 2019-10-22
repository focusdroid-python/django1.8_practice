# Django笔记

## 安装虚拟环境
    ```
        > 0. sudo pip insall virtualenv # 安装虚拟环境
        > 1. sudo pip install virtualenvwrapper # 安装虚拟环境扩展包
        >2. 修改根目录下面的 .bashrc 在最地下添加
        export WORKON_HOME=$HOME/.virtualenvs
        export VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3.6' # python3.x需要指定版本
        source /usr/local/bin/virtualenvwrapper.sh
        >3. 使用source .bashrc使其生效一下
        -- 创建虚拟环境
            mkvirtualenv -p python3 虚拟环境名字  # python3的环境
        --进入虚拟环境
            workon 虚拟环境名字
        --退出虚拟环境
            deactivate
        --删除虚拟环境
            rmvirtualenv 虚拟环境名字
        > 4. 虚拟环境安装包
            pip3 install # 包名字
    ```
## 创建django项目
```
    使用命令创建项目:
        dhango-admin startproject 项目名字
         setting.py 项目的配置文件
         url.py 路由的配置 
         wsgi.py  wsgi协议，web服务器和Django交互的入口
         manage.py 项目的管理文件
    创建应用: 
        python manage.py startapp 应用名
          __init__ 说明目录是一个python模块
          models.py 和数据库项目的内容
          views.py 接受请求，进行处理,与M和T进行交互,返回应答
          test.py 测试代码
          admin.py 网站后台相关

    注册应用：如下
        INSTALLED_APPS = (
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'booktest', # 注册应用
        )
    运行项目： 
        python manage.py runserver
        python manage.py runserver:8888 # 指定端口号
```    
## ORM框架
### Object(对象-类)-Relations(关系，关系数据库中的表)-Mapping(映射)
```
> django中内嵌ORM框架，ORM框架可以将数据表进行对应起来， 只需要通过类和对象就可以经inx进行数据表进行操作
> 设计类： 模型类
> ORM 另外一个作用， 根据设计的类自动生成数据库中的表


在根目录/booktest/models.py
# 图书类
class BookInfo(models,MOdel):
    '''图书模型类'''
    # CharField说明是一个字符串， max_length指定字符串的最大长度
    btitle = models.CharField(max_length=20)
    # 出版日期， DateField说明是一个日期类型
    bpub_date = models.DateField()
> 生成迁移文件
    python manage.py makemigrations
> 执行迁移生成表
    python manage.py migrate
```

## 通过模型类操作数据表
```
> 进入项目shell命令：
    python manage.py shell
>>> from booktest.models import BookInfo
>>> b=  BookInfo()
>>> b.btitle = '天龙八部'
>>> from datetime import date
>>> b.pub_date = date(1990,1,1)
>>> b.save()

# 英雄人物类
# 英雄名 hname
# 性别 hgender
# 年龄 hage
# 备注 hcomment
# 关系属性 book，建立图书类和英雄人物类之间的一对多关系
class HeroInfo(models.Model):
    '''英雄人物类'''
    hname = models.CharField(max_length=20)
    # 性别，BooleanField说明bool类型，default指定默认值， False代表男， Tru代表女
    hgender = models.BooleanField(default=False)
    # 备注
    hcomment = models.CharField(max_length=128)
    # 关系属性， hbook建立图书类和英雄人物之间的一对多关系
    hbook = models.ForeignKey('BookInfo') # 外键

```
## 后台管理
```
> 1. 本地化
    语言和时区的本地化
    修改setting文件
        # LANGUAGE_CODE = 'en-us'
        LANGUAGE_CODE = 'zh-hans' # 使用中文
        
        # TIME_ZONE = 'UTC'
        TIME_ZONE = 'Asia/Shanghai' # 中国时间
> 2. 创建管理员
    命令： python manage.py createsuperuser
> 3. 注册模型类
    在应用下的admin.py中注册模型类
    告诉django框架根据注册的模型类来生成对应表的管理页面
    b = BookInfo()
    str(b)__str++
```

## 视图
```
在django中，通过浏览器去请求一个页面时，去处理
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse('success')

```
## 模板
```
### 模板文件夹的使用
> 1.创建模板文件夹
    在项目根目录创建templates
> 1.配置模板目录
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')], # 设置文件目录
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
> 3. 使用模板文件
    加载模板目录
        去模板目录下获取html文件的内容，得到一个模板对象
    定义模板上下文
        向模板传递数据
    模板渲染
        得到一个标准的html内容
    def index2(request):
        # 1. 加载模板文件， 模板对象
        temp = loader.get_template('booktest/index.html')
        # 2. 定义模板上下文: 给模板传递数据
        context = RequestContext(request, {})
        # 3。 模板渲染
        res_html = temp.render(context)
        # 4。 返回应答
        return HttpResponse(res_html)

    封装之后的：
        def my_render(request, template_path, context_dict={}):
            '''使用模板文件'''
            # 1. 加载模板文件， 模板对象
            temp = loader.get_template(template_path)
            # 2. 定义模板上下文: 给模板传递数据
            context = RequestContext(request, context_dict)
            # 3。 模板渲染
            res_html = temp.render(context)
            # 4。 返回应答
            return HttpResponse(res_html)
        
        def index2(request):
            return my_render(request, 'booktest/index.html', {'content': 'Hello Django'})

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>首页</title>
        </head>
        <body>
        <h1>这是django项目的第一个应用</h1>
        <h3>模板数据: {{content}}</h3>
        <h4>----------------------------------------</h4>
        <div>{{list}}</div>
        <div>
            <div>for循环</div>
            <ul>
                {% for i in list %}
                    <li>{{ i }}</li>
                {% endfor %}
            </ul>
        </div>
        </body>
        </html>
> 3.
> 3.

```
## 配置mysql数据库
```
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'bj18', # 数据库名称
        'USER': 'root', # 连接数据库用户名
        'PASSWORD': 'mysql', # 对应的密码
        'HOST': 'localhost', # 指定mysql数据库所在的ip
        'PORT': 3306, # 对应的端口
    }
}

// 在test2/__init__.py
    import pymysql
    pymysql.install_as_MySQLdb()
### 在booktest中新建模型类
    class BookInfo(models.Model):
        '''图书模型类'''
        btitle = models.CharField(max_length=20)
        # 出版日期
        bpub_date = models.DateField()
        # 阅读量
        bread = models.IntegerField(default=0)
        # 评论量
        bcomment = models.IntegerField(default=0)
        # 删除标记
        isDelete = models.BooleanField(default=False)
    
    class HeroInfo(models.Model):
        '''英雄人物模型类'''
        #英雄名
        hname = models.CharField(max_length=20)
        #  性别
        hgender = models.BooleanField(default=False)
        # 备注
        hcomment = models.CharField(max_length=200)
        # 关联属性
        hbook = models.ForeignKey('BookInfo')
        # 删除标记
        isDelete = models.BooleanField(default=False)

    > 输入完成之后：
        python manage.py makemigrations // 生成迁移文件
        python manage.py migrate // 生成表

    > 页面重定向：
        from django.shortcuts import render, redirect
        from django.http import HttpResponse, HttpResponseRedirect

```
## 字段属性和选项
```
AutoField   自动增长的IntegerField，通常不用指定，不指定时django会自动创建属性为id为自动增长属性

BooleanField  布尔字段， 数值为True  False

NullBooleanField  支持Null  True   False

CharField(max_length=最大长度) 字符串，参数max_length表示最大字符个数

TextFiels   大文本字段，一般超过4000字是使用

IntegerField   整数

DecimalField(max_digits=None, decimal_places=None)  十进制浮点数， 参数max_digits表示总位数， decimal_places表示小数位数

FloatField  浮点数，参数同上（本质区别，精度不同，一般精度使用这个，特殊精度使用上面DecimalField）

DateField([auto_now=False, auto_now_add=False])
auto_now, 自动设置该字段为当前时间用于最后一次 修改 的时间戳，更新的时间
auto_now_add 第一次创建时自动设置当前时间，用于 创建 的时间戳

TimeField  时间 ，参数同上
DateTimeField  日期时间， 参数同DateField(年月日时分妙)

FileField  上传文件的字段
ImageField  继承于FileField，对上传的内容进行校对，确保是有效的图片

```
## 选项
```
default 默认值

primary_key 若为True, 则该字段成为模型的主键字段，默认值是False，一般作为AutoField的选项使用

unique  如果为True，这个字段在表中有唯一值，默认值False

db_index 如果为True，则会在表中为此字段创建索引，默认值False

db_column 字段的名称，如果未指定，则使用属性名称

null 如果为True，表示允许为空，默认值False

blank 如果为True，该字段允许为空白，默认值False

```
## 后台管理
```
> 1. 本地化
    语言和时区
    修改setting.py文件
> 2. 创建管理员
    python manage.py createsuperuser
> 3. 注册模型类
    在应用下admin.py中注册模型类
    告诉django框架根据注册的模型类对应表管理页面
    b = BookInfo()
    str(b) __str__
> 4. 自定义管理页面
    自定义模型管理类，模型管理类就告诉django在生成管理页面上显示哪些内容

在应用下面的admin.py文件：
    '''这样就可以在之前创建的管理页面中使用这个HeroInfo这个表了'''
    from booktest.models import HeroInfo
    admin.site.register(HeroInfo)

```
## 设置数据库日志
```
> 修改mysql的日志文件，让其产生mysql.log，即是mysql的日志文件，里面记录mysql数据库的操作记录i
> 1. 使用下面的命令打开mysql的配置文件，去除68，69行的注释
    sudo vi /etc/mysql/mysql.conf.d/mysqld.cnf
> 2. 重启mysql服务，就会产生mysql的日志文件
    sudo service mysql restart
> 3. 打开mysql的日志文件
    /var/log/mysql/mysql.log是mysql日志文件所在位置
> 4. 使用下面命令可以实时查看mysql的日志文件
    sudo tail -f /var/log/mysql/mysql.log

```
## 数据库授权
```
grant all privileges test6.* to 'root'@'192.168.1.108' identified by 'mysql' with grant option;
flush privileges

test6.*数据库名称
'root'@'192.168.1.108' root账户，和给ip授权
```
## 查询函数(通过模型类查询数据库)
```
> 通过模型类.objects属性可以调用如下函数，实现对模型类对应的数据表的查询

get  返回表中满足条件且只能是一条数据       返回值是一个模型类对象     1》如果查到多条数据，则抛异常MultipleObjectsReturned 2》查询不到数据，则抛异常DoesNotExist

all  返回模型类对应表中所有数据          返回值是一个QuerySet      查询集

filter  返回满足条件的数据            返回值是一个QuerySet       参数写查询条件

exclude  返回不满足条件的数据          返回值是一个QuerySet      参数写查询条件

order_by  对查询结果进行排序          返回值是一个QuerySet      参数中写根据哪些字段进行排序

判等： exact
BookInfo.objects.get(id=1)
BookInfo.objects.get(id__exact=1)

模糊查询： contains   mysql  like
    BookInfo.objects.filter(btitle__contains='传')
以什么开头以什么结尾： startswitch    endswitch
  

空查询  isnull
    select * from booktest_bookinfo where btitle is not null;
    BookInfo.objects.filter(btitle__isnull=False)


范围查询  in
    select * from booktest_bookinfo where id in (1,2,3,5)
    BookInfo.objects.filter(id__in = [1,2,3,5])

比较查询: gt(greate than)  lt(less than)  gte(equal)大于等于  lte 小于等于
    select * from booktest_bookinfo where id > 3;
    BookInfo.objects.filter(id__gt=3)

日期查询：
    BookInfo.objects.filter(bpub_date__year = 1980)

    查询1980.1.1以后发表的图书
    from datetime import date
    BookInfo.objects.filter(bpub_date__gt=date(1980,1,1))

exclude方法示例:
    查询id不为3的图书信息
    BookInfo.objects.exclude(id=3)

order_by 方法示例
    查询所有图书信息， 按照id从小到大进行排序
    BookInfo.objects.all().order_by('id')
    BookInfo.objects.order_by('id')

     查询所有图书信息， 按照id从大到小进行排序
    BookInfo.objects.all().order_by(-'id')
    BookInfo.objects.order_by(-'id')
```
##  Q对象 用于查询条件之间的逻辑关系
```
作用： 用于查询条件之间的逻辑关系， not and or  可以对Q对象进行 & | ~ 操作

使用之前先导入：
    from django.db.models import Q
    且
    BookInfo.objects.filter(id__gt=3, bread__gt=30)
    BookInfo.objects.filter(Q(id__gt=3) & Q(bread__gt=30))
    或
    BookInfo.objects.filter(Q(id__gt=3) | Q(bread__gt=30))
    非
    查询id不等于3图书信息
    BookInfo.objects.filter(~Q(id3))
```

## F对象 用于类属性之间的比较
```
作用：用于类属性之间的比较
from django.db.models import F

查询图书阅读量大于评论量图书信息
BookInfo.objects.filter(bread++gt=F('bcomment'))
查询图书阅读量大于2倍评论量图书信息
BookInfo.objects.filter(bread++gt=F('bcomment') * 2)
```

## 聚合函数 aggregate 返回值一个字典
```
sum count avg max min

aggregate: 调用这个函数来使用聚合，返回值一个字典

使用之前先导入聚合类：
    from django.db.models import Sum,Count, Max, Min, Avg

>>> BookInfo.objects.all().aggregate(Count('id'))
{'id__count': 8}
>>> BookInfo.objects.all().aggregate(Count('bread'))
{'bread__count': 8}

```
### 注意： 对一个QuerySet实例对象，可以继续调用上面的所有函数

## 查询集
```
查询集特性：
> 1. 惰性查询： 只有在实际查询集中的数据的时候才会发生数据库的真正查询
> 2. 缓存： 当使用的是同一个查询集时，第一次查询的时候会发生实际数据库的查询，然后缓存起来，之后在使用这个查询集时，使用的是缓存中的结果

限制查询集：
    可以对一个查询集进行切片或者取下标
    对一个查询集进行切片操作会产生一个新的查询集，下标不允许为负数


取出查询集第一条数据的两种方式：
    b[0]                如果b[0]不存在，会抛出IndexError异常
    b[0:1].get()        如果b[0:1].get()不存在，会抛出DoesNotExist异常
exists: 判断一个查询集中是否有数据。 True False
```
## 10 模型类关系
```
> 1. 一对多关系
modles.ForeignKey()  定义在多的类中
> 1. 多对多
models.ManyToManyField()  定义在哪个类都可以
> 1. 一对一
models.OneToOneField()  定义在哪个类都可以

```

## 关联查询
```
在一对多关系中，一对应类叫做一类，多对应的那个类我们叫做多类，我们把多类中定义关联的类属性叫做关联属性
通过模型类进行关联查询：
    查询图书信息，要求所有关联英雄的描述包含‘八’
    BookInfo.objects.filter(heroinfo__hcomment__contains='八')
    
    查询图书信息，要求图书中的英雄id大于3
    BookInfo.objects.filter(heroinfo__id__gt=3)

    查询书名为天龙八部的所有英雄
    HeroInfo.objects.filter(hbook__btitle='天龙八部')
注意：
    >1. 通过模型类实现关联查询时，要查那个表中的数据就需要哪个类来查
    >2. 写关联查询条件的时候，如果类中没有这个关系，条件需要对应类的名，如果类中有关系属性，直接写关系属性
```
## 插入，更新，删除
```
>1. 调用一个模型类对象save方法的时候就可以实现对模型类对应数据表的插入和更新
>2. 调用一个模型类的delete方法的时候就可以实现对模型类对应数据表数据的删除
```
## 自关联
```
子关联本质就是一对多的关系

class AreaInfo(models.Model):
    '''地区模型类'''
    # 地区名称
    atitle = models.CharField(max_length=20)
    # 关系属性，代表当前地区的父级地区
    aParent = models.ForeignKey('self', null=True, blank=True)

def area(request):
    '''获取广州市的上级地区和下级地区'''
    # 1 获取广州市的信息
    area = AreaInfo.objects.get(atitle='广州市')
    # 2 查询广州市的上级地区
    parent = area.aParent
    # 3. 广州市的下级地区
    children = area.areainfo_set.all()
    # 使用模板
    return render(request, 'booktest/area.html', {'area': area, 'parent': parent})

一类 BookInfo      多类  HeroInfo
一类---》多类   hhbook
多类---》一类   b.heroinfo_set.all()


```
## 15 元选项
```
解决模型类不依赖表名，指定表名

以下内容只能改变bookinfo
class Meta:
    db_table = 'bookinfo'

即使模型类BookInfo名字改变之后也不会依赖应用名称

class BookInfo(models.Model):
    '''图书模型类'''
    btitle = models.CharField(max_length=20)
    # 出版日期
    bpub_date = models.DateField()
    # 阅读量
    bread = models.IntegerField(default=0)
    # 评论量
    bcomment = models.IntegerField(default=0)
    # 删除标记
    isDelete = models.BooleanField(default=False)

    # book = models.Manger()
    objects = BookInfoManager()

    # @classmethod
    # def create_book(cls, btitle, bpub_date):
    #     # 1. 创建一个图书对象
    #     obj = cls()
    #     obj.btitle = btitle
    #     obj.bpub_date = bpub_date
    #     obj.save()
    #     return obj
    class Meta: # class Meta： db_table是固定的， 
        db_table = 'bookinfo'


```
## 视图
```

django上线之前要做的以下几点：
    DEBUG 修改为 false
    修改ALLOWED_HOSTS = ['*']
```

## 捕获url参数
```
>1. 位置参数 
        url(r'^showarg(\d+)$', views.showarg), # 捕获url参数
        http://127.0.0.1:8000/showarg22  # 22
>2. 关键字参数
    ?P<组名>
    关键字参数，视图中必须和正则表达式组名一致
        url(r'^showtwo(?P<num>\d+)$', views.showtwo),

        def showtwo(request, num):
            return HttpResponse(num)
        
        http://127.0.0.1:8000/showtwo456 # 456
```

## 获取登录用户名和密码
```
    ## request.POST 保存的是post方式提交的参数 
    ## request.GET 保存的是get方式提交的参数 两者都是QueryDict  字典类型的值，但是一个键可以对应多个值
    # request.method请求方式
    print(request.method)
    # request.path 只显示路由地址，不显示参数和域名
    print(request.path)



    # 1. 获取用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username+'---'+password)
    # 2. 进行登录校验
    # 实际的情况：根据用户名和密码查找数据库
    # 模拟: tree   111
    if username == 'tree' and password == '111':
        return redirect('/index')
    else:
        return redirect('/login')

    # 3. 返回应答
    return HttpResponse('ok')

配置静态目录
在项目根目录中创建static目录
在settings中最后添加：
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # 设置静态保存目录

```
## 状态保持 cookie
```
cookie 保存在浏览器端
>1. 以键值对形式存储
>2. 通过浏览器访问一个网站时，会将浏览器存储的跟网站相关的所有cookie信息发送给网站的服务器， request.COOKIES 
>3. cookie是基于域名安全的 
>4. cookie是过期时间的，如果不指定，默认浏览器关闭之后cookie就过期 
过期时间设置：
response.set_cookie('num', 1, max_age=14*24*3600)
# response.set_cookie('num', 1, expires=datetime.now()+timedelta(day=14))

设置cookie需要一个HttpResponse类的对象或者是它子类的对象:
    HttpResponse, JsonResponse

def set_cookie(request):
    '''设置cookie信息'''
    response = HttpResponse('设置cookie')
    response.set_cookie('num', 1)
    return response

def get_cookie(request):
    '''获取cookie'''
    num = request.COOKIES['num']
    return  HttpResponse(num)

```
## 状态保持 session
```
session保存在服务器端 依赖cookie
session 过程
浏览器访问网站 ----》进行设置session信息------》django_session这个表里面  session_id: session_data --->
设置一个cookie sessionid ----->返回应答让浏览器保存sessionid 唯一表示码------》在访问网站的时候获取sessionid根据sessionid的值取出对应的session信息
request.session

设置session: request.session['username'] = 'tree'
获取session： request.session['username']
根据键值取值： request.session.get('健', 默认值)
清楚所有session，并在存储中删除值部分 request.session.clear()
清除session数据，在存储中删除session整条数据： request.session.flush()

删除session中指定的键和值，在存储中删除session的整条数据： del request.session['键']

request.session.set_expiry(value)
如果value是一个整数，会话session_id cookie 将在value秒之后过期
如果value是一0，会话session_id cookie 将在浏览器关闭之后过期
如果value是None（不设置），会话session_id cookie 将在14天之后过期

>1. session以键值对进行存储
>1. session依赖cookie，唯一的标识码sessionid 保存在cookie中
>1. session也有过期时间， 如果不指定，默认两周过期

```
## cookie和session的应用场景
```
cookie: 记住用户名，安全性不高
session： 涉及到安全性要求比较高的数据， 银行卡账户，密码
```

## 模板
```
>1. 首先去配置的模板目录下面去找模板
>2. 去INSTALLED_APPS下面的每个应用的去找模板文件，前提应用中必须有templates文件夹

模板的取值：
    把book当成一个字典，把btitle当成键名，进行取值book['btitle']
    把book当成一个对象，把btitle当成一个属性，进行取值 book.btitle
    把book当成一个对象，把btitle当成对象的方法，进行取值 book.btitle
使用模板变量的时候，前面可能是一个字典，可能是一个对象，可能是一个列表


模板标签：

登录装饰器：
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

csrf伪造攻击:
>1. 默认打开csrf中间件
>2. 表单post提交数据时加上{% csrf_token %}标签 

> 1. 登录正常的网站之后你的浏览器保存的session，你没有退出
> 2. 你有访问另外一个网站， 并且点击页面上的按钮
# csrf只针对post进行防护
    <form method="post" action="/change_pwd_action">
        {% csrf_token %}
        新密码: <input type="password" name="pwd">
        <input type="submit" value="确认修改">
    </form>

防御原理:
>1. 渲染模板文件时在页面上生成一个名字叫做csrfmiddlewaretoken的隐藏域
>2. 服务器交给浏览器保存一个csrftoken的cookie信息
>3. 提交表单时，两个值都会发给服务器，服务器进行比对，如果一样，则csrf验证通过，否则失败 



```
## 验证码
```
pip3 install Pillow==3.4.1
如果安装pillow出错https://blog.csdn.net/shaququ/article/details/54292017
```
## url反向解析
```
    url(r'^', include('booktest.urls', namespace='booktest')), 添加namespace=‘booktest’ 一般都是应用名

在应用中的urls中：
    url(r'^index$', views.index, name='index'), 添加name
正常的：
<h1><a href="/index">首页</a></h1>

<div>url反向解析生成index链接，不受html文件名限制，只通过name属性</div>
<h1><a href="{% url 'booktest:index2' %}">首页</a></h1>

普通参数和关键字参数
<a href='{% url 'booktest:show_args' 1 2 %}'></a>
<a href='{% url 'booktest:show_args' c=1 d=2 %}'></a>

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
```
## 静态文件
```
配置静态文件所在的物理目录， setting.py
STATIC_URL = '/static'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_URL 设置静态文件对应的url
STATICFILES_DIRS 设置静态文件所在的物理目录

<!DOCTYPE html>
{% load staticfiles %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>image</title>
    <style>
        .img {
            width: 500px;
        }
    </style>
</head>
<body>
<div>
    <img src="/static/image/timg.jpeg" class="img" alt=""> <br/>
    动态获取，拼接静态文件的路径：<br/>
    <img src="{% static 'image/timg.jpeg' %}" class="img" alt="">
</div>
</body>
</html>

```

## 中间件 test5项目
```
中间件函数是django框架给我们预留的函数接口，让我们可以干预请求和应答过程
获取浏览器端的ip地址：
    使用request对象的META属性：request.META['REMOTE_ADDR']

使用中间件：
    

禁止IP访问：
EXCLUDE_IPS = ['192.168.0.9']
def index2(request):
    '''首页'''
    # 获取浏览器端的ip地址
    user_ip = request.META['REMOTE_ADDR']
    if user_ip in EXCLUDE_IPS:
        return render(request, 'booktest/ip.html')
    else:
        return render(request, 'booktest/index2.html')

使用装饰器实现：
EXCLUDE_IPS = ['192.168.0.9']
def blocked_ips(view_func):
    def wrapper(request, *view_args, **view_kwargs):
        user_ip = request.META['REMOTE_ADDR']
        if user_ip in EXCLUDE_IPS:
            return render(request, 'booktest/ip.html')
        else:
            return view_func(request, *view_args, view_kwargs)
    return wrapper

# request 和视图的request视图一样
# view_func 要调用哪个视图函数
# *view_args 视图函数的位置参数
# **view_kwargs 视图函数的关键字参数

通过django来实现封禁IP：（全局过滤）
>1. 新建middleware.py文件， 
>2. 在建应用的下面新建， process_view是django指定的，不能改变,还有必须定义在类里面
>3. 注册这个类，在setting.py中：
    MIDDLEWARE_CLASSES = (
         ...
        'booktest.middleware.BlockedIPSMiddleware', # 注册中间件类
    )
在类中定义中间件预留函数：
    __init__: 服务器响应第一个请求的时候调用
    process_request: 是在产生request对象，进行url匹配之前调用
    precess_view: 是url匹配之后，调用视图函数之前
    process_exception: 视图函数出现异常，内容返回给浏览器之前，会调用这个函数。
        如果注册的多个中间件类中包含process_exception函数的时候，
        调用的顺序跟注册的顺序是相反的
            --------调用异常222222222222222222222222222&******************************
            --------调用异常&1111111111111111111111111******************************



1. 产生request对象
2. 调用中间件类中的process_request
3. 通过url找对应的视图
4. 调用中间件process_view
5. 调用view
6. 调用中间件类中的process_response

```
## admin后台管理
```
models.py: # test5
    class AreaInfo(models.Model):
    '''地址模型类'''
    atitle = models.CharField(max_length=20)
    # 自关联属性
    aParent = models.ForeignKey(BookInfo, null=True, blank=True)

    def __str__(self): # 显示这张表结构的名称
        return self.atitle
```
## 上传文件设置
```
>1. 在static下面新建midia文件夹
# 设置上传保存目录
>2. MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

### 用户自定义上传图片：
    > 使用表单上传，必须是post
    > 制定编码类型：enctype='multipart/from-data'


上传文件不大于2.5M放在内存中，如果有大于2.5M放在临时的文件中
print(type(pic))
# <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
# <class 'django.core.files.uploadedfile.TemporaryUploadedFile'>
    # 1。 获取上传文件的处理对象
    pic = request.FILES['pic']
    # 2. 创建一个文件
    # 3. 获取上传文集爱你的内容，并写入到创建的文件中
    # 4. 在数据库保存上传记录
    # 5. 返回
django文件上传处理类：
    print(settings.FILE_UPLOAD_HANDLERS)



def upload_handle(request):
    '''接受上传图片'''
    # 1。 获取上传文件的处理对象
    pic = request.FILES['pic']

    # 2. 创建一个文件
    save_path = '%s/booktest%s'%(settings.MEDIA_ROOT, pic.name)
    with open(save_path, 'wb') as f:
        # 3. 获取上传文件的内容，并写入到创建的文件中
        for content in pic.chunks():
            f.write(content)

    # 4. 在数据库保存上传记录 print(random.randint(0,9))
    num = random.randint(0, 9)
    PicTest.objects.create(goods_pic='booktest%d/%s'%(num, pic.name))
    # 5. 返回
    return HttpResponse('ok')
```
## 分页
```
from django.core.paginator import Paginator
Paginator类对象的属性：
    num_pages: 返回分页之后的总页数
    page_range: 返回分页之后的页码列表

Pagintor类对象的方法：
    page(self, number): 返回第number页的Page类实例对象

Page类对象的属性：
    number: 返回当前页的页码
    object_list: 返回包含当前页数据的查询集
    paginator: 返回对应的pagintor对象

Page类对象的方法：
    has_previcus: 判断当前页是否有前一页
    has_next: 判断当前页是否含有下一页
    previous_page_number: 返回前一页的页面
    next_page_number: 返回下一页的页码
    

```

## redis数据库
```
http://www.redis.cn/download.html
Redis特性:
Redis与其他key-value缓存产品有一下三个特点
    支持数据持久化,可以将内存中的数据保存在磁盘中，重启的时候可以再次进行加载进行使用
    不仅仅支持支持简单的key-value类型的数据，同时还提供list，zset，hash等数据结构存储
    支持数据备份，即master-slave模式的数据备份

Redis优势：
性能极高，Redis能读的速度是110000次/s, 写的速度81000次/s
丰富的数据类型，Redis支持二进制案例String，Lists， Hashes, Sets
及 Ordered Sets数据类型操作
原子 Redis的所有操作都是原子性，同时Redis还支持对几个操作全并后的原子性执行

Redis应用场景：
    用来做缓存--redis的所有数据是放在内存中的（内存数据库）
    可以用在某些特定应用场景下替代传统数据库--比如社交类应用
    在一些应用大型系统中，巧妙的实现特定的功能，session共享，购物车
    

Redis下载安装
    wget http://download.redis.io/releases/redis-3.2.8.tar.gz
    
    tar -zxvf redis-3.2.8.tar.gz

    sudo mv ./redis-3.2.8/usr/local/redis

    cd /usr/local/redis

    sudo make

    sudo make test(测试安装环境)
    
    sudo make install（安装可执行程序，安装在/usr/local/bin这个目录下方）

    安装完成之后，检查安装：
        cd /usr/local/bin
        ls -all
        查看是否安装上redis-cli redis-server
    
    配置文件目录：
        sudo cp ./redis.conf /etc/redis/redis.conf

redis-server redis服务器
redis-cli redis命令行客户端
redis-benchmark redis性能测试工具
redis-check-aof AOF文件修复工具
redis-check-rdb RDB文件检索工具
    
    

如果报错：
You need tcl 8.5 or newer in order to run the Redis test.
安装Redis，运行make test的时候出错：

You need tcl 8.5 or newer in order to run the Redis test
make: *** [test] Error 1

安装tcl就行了：

复制代码
wget http://downloads.sourceforge.net/tcl/tcl8.6.9-src.tar.gz
sudo tar xzvf tcl8.6.9-src.tar.gz -C /usr/local/
cd /usr/local/tcl8.6.9/unix/
sudo ./configure
sudo make
sudo make install
    
```
## redis核心配置项
```
查看/etc/redis/redis.conf下：
    sudo vi /etc/redis/redis.conf
绑定ip：如果远程访问，可将此行注释，或绑定一个真实ip
    bind 127.0.0.1

端口： 默认6379
    port 6379

是否以守护进程进行:
    如果是守护进程，则不会在命令行阻塞，类似于服务
    如果是非守护进程，则当前终端被阻塞
    设置为yes表示守护进程，设置no表示非守护进程
    推荐使用yes
    daemonize yes

数据文件:
   dbfilename dumo.rdb

数据文件存储路径：
    dir /var/lib/redis
日志文件：
    logfile /var/log/redis/redis-server.log

数据库：默认是16个
    database 16

主从复制，类似于双机备份
    slaveof
```
## redis服务器端
```
服务器端命令是： redis-server
可以使用帮助文档：
    redis-server --help

推荐使用服务方式管理redis服务
启动:
    sudo service redis start

停止：
    sudo service redis stop

重启： sudo service redis restart

个人习惯：
    ps -ef | grep redis 查看redis服务器进程
    sudo kill -9 pid 杀死redis服务器
    sudo redis-server /etc/redis/redis.conf 指定加载的配置文件
```
## redis客户端
```
客户端的命令为redis-cli
连接redis：
    redis-cli
运行测试命令：
    ping

切换数据库：
数据库没有名称，默认只有16个，通过0-15来标识，连接redis默认选择第一个数据库
select n


值类型分为5种：
字符串string
哈希 hash
列表 list
集合 set
有序集合 zset

保存：
    set key value
设置键值过期时间：
    setex aa 3 bb

设置多个键值：
    mset a1 python a2 java a3 javascript
追加值：
    append key value

获取：
获取单个key的值：
    get key
一次获取多个值：
    mget key1 key2 ...

键命令：
keys pattern

查看所有键:
    keys *
判断键命令是否存在：
    exists key
查看value的类型：
    type key

删除：
删除键及对应的值：
    del key1 keys
设置过期时间:
    expire key seconds
    expire a1 300
查看过期时间：
    ttl key


hash类型：
hash用于存储对象，对象的结构为属性，值
值的类型为string

增加，修改：
设置单个属性：
    hset key field value
设置键user的属性name为tree
    hset user name tree
 
设置多个属性：
hmset key field1 value field2 value
hmset u2 name tree age 12

获取：
hkeys key
hkeys u2  // name age
获取多个属性值：
hmget key field1 field2
hmget u2 name age

获取所有属性的值：
hvals key
hvals u2


删除：
删除整个hash键，使用del命令
hdel key field1 field2
hdel u2 age

解决某些小问题：
强制关闭redis快照导致不能持久化，
config set stop-writes-on-bgsave-error no
```

```
list类型
特点:
列表的元素类型是string
按照插入顺序排序
增加：
在左侧插入数据
lpush key value1 value2
lrange key start end
在右侧插入数据
rpush key value1 value2

在指定元素前或者后插入新元素
linsert key before或after 现有元素 新元素

删除
count > 0 从头往尾移除
count < 0 从尾往头移除
count = 0 移除所有
lrem key count value


set类型
无序集合
元素为string类型
元素句具有唯一性
说明：对于集合没有修改操作


增加：
sadd key member1 member2

获取
smembers key

删除
srem key

zset
有序集合
元素为string类型
元素句具有唯一性
每个元素都会关联一个double类型的score，表示权重，通过权重将元素从小到大排序

说明：对于集合没有修改操作

```
## ubuntu安装redis
```
> redis安装:
1. 进入虚拟环境，
    pip3 install redis

> 调用模块
引入模块：
from redis import *
这个模块提供了StrictRedis对象（Strict严格），用于连接服务器，并按照不同类型提供不同的方法进行交互操作 
String
    set
    setex
    mset
    append
    get
    mget
    key

keys:
    exists
    type
    delete
    expire
    getrange
    ttl
hash:
    hset
    hmset
    hkeys
    hget
    hmget
    hvals
    hdel

list:
    lpush
    rpush
    linsert
    lrange
    lset
    lrem
set:
    sadd
    smembers
    srem
zset:
    zadd
    zrange
    zrangebyscore
    zscore
    zrem
    zremrangebyscore

### 准备
创建一个redis目录
创建redis_string.py
from redis import StrictRedis


if __name__ == '__main__':
    # 创建StrictRedis对象，链接redis数据库
    try:
        sr = StrictRedis()
        # 添加一个key，为name, value, focusdroid
        res = sr.set('name', 'focusdroidss')

        res = sr.set('name', 'nangong')
        # 获取name的值
        rss = sr.get('name')
        print(rss)
    except Exception as e:
        pass

使用redis存储session：
session的redis配置
1. 安装pip3 install django-redis-sessions==0.5.6
2. 修改settings文件,增加如下项:
    # 设置redis存储redis信息
    SESSION_ENGINE = 'redis_sessions.session'
    # redis服务的ip地址
    SESSION_REDIS_HOST = 'localhost'
    # redis服务的端口号
    SESSION_REDIS_PORT = 6379
    # redis中哪一个数据库
    SESSION_REDIS_DB = 2
    # 链接数据库密码
    SESSION_REDIS_PASSWORD = ''
    # session: 唯一标识码
    SESSION_REIS_PREFIX = 'session'
    

```
## 搭配redis主从服务器
```
> 1. 配置主服务器
修改/etc/redis/redis.conf文件
sudo vi /etc/redis/redis.conf
bind 192.168.1.108（服务器ip）
重启服务器
redis-server redis.conf
但是最新版本的redis需要这样启动：
redis-cli -h 192.168.1.108 -p 6379

使用ps -aux | grep redis 查看


> 2. 配置从服务器

```

## 天天生鲜项目



















## 生成迁移文件
    python manage.py makemigrations
## 执行迁移生成表
    python manage.py migrate
    
## 通过模型类生成数据表
    # 项目shell环境
    python manage.py shell
    
    
```
insert into booktest_bookinfo(btitle, bpub_date, bread, bcomment, isDelete) values
('射雕英雄传', '1980-5-1', 12, 34, 0),
('天龙八部', '1986-7-24', 36, 40, 0),
('笑傲江湖', '1995-12-24', 20, 80, 0),
('雪山飞狐', '1987-11-11', 58, 24, 0);

insert into booktest_heroinfo(hname, hgender, hbook_id, hcomment, isDelete) values
('郭靖', 1, 1, '降龙十八章', 0),
('黄蓉', 0, 1, '打狗棍法', 0),
('黄药师', 1, 1, '弹指神通', 0),
('欧阳锋', 1, 1, '蛤蟆功', 0),
('梅超风', 0, 1, '九阴白骨爪', 0),
('乔峰', 1, 1, '降龙十八掌', 0),
('王语', 1, 2, '神仙姐姐', 0);
```
