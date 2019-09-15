from django.db import models

# Create your models here.

class BookInfoManager(models.Manager):
    '''图书模型管理类'''
    # 改变查询的结果集
    def all(self):
        # 1. 获取所有的数据，调用父类的all方法
        books = super().all() # QuerySet
        # 2. 对数据进行过滤
        books = books.filter(isDelete = False)
        # 3. 返回books
        return books

    # 2. 封装函数：操作模型类对应的数据表（增删改查）
    def create_book(self, btitle, bpub_date):
        # 创建一个对象
        # book = BookInfo() # BookInfo模型类名不变的情况
        # 获取self所在的模型类
        model_class = self.model # 获取模型类名
        book = model_class()
        book.btitle = btitle
        book.bpub_date = bpub_date

        book.save()

        return book



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

# # 新闻类型类
# class NewsType(models.Model):
#     # 类型名
#     type_name = models.CharField(max_length=20)
#
# # 新闻类
# class NewsInfo(models.Model):
#     title = models.CharField(max_length=128)
#     # 发布时间
#     pub_date = models.DateTimeField(auto_now_add=True)
#     # 信息内容
#     content = models.TextField()
#     # g关系属性
#     news_type = models.ManyToManyField('NewsType')

class AreaInfo(models.Model):
    '''地区模型类'''
    # 地区名称
    atitle = models.CharField(max_length=20)
    # 关系属性，代表当前地区的父级地区
    aParent = models.ForeignKey('self', null=True, blank=True)

    # 使用元类，创建表名
    # class Meta:
    #     db_table = 'areas' # 表名



















