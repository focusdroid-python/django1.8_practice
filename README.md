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











## 生成迁移文件
    python manage.py makemigrations
## 执行迁移生成表
    python manage.py migrate
    
## 通过模型类生成数据表
    # 项目shell环境
    python manage.py shell
    
    
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
    
