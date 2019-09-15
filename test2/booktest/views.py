from django.shortcuts import render, redirect
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

def delete(request, did):
    '''删除点击的图书'''
    # 1. 通过did获取图书对象
    book = BookInfo.objects.get(id=did)
    # 2. 删除
    book.delete()
    # 3. 重定向，让浏览器访问 /index
    # return HttpResponseRedirect('/index')
    return redirect('/index')

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