from django.db import models

# Create your models here.

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