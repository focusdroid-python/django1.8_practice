from django.shortcuts import render
from booktest.models import BookInfo
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def index(request):
    '''显示图书信息'''
    # 1. 查询所有的图书信息
    books = BookInfo.objects.all()
    # 2。 使用模板
    return render(request, 'booktest/index.html', {'books': books})

def create(request):
    '''新增一本书'''
    b = BookInfo()
    b.btitle = '同学两亿岁'
    b.bpub_date = date(1990,1,1)
    # 保存进数据库
    b.save()
    # 返回应答
    # return HttpResponse('ok')
    return HttpResponseRedirect('/index') # 让浏览器自动返回/index页面