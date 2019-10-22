from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def set_session(request):
    '''设置session'''
    request.session['username'] = 'tree'
    request.session['sex'] = True

    return HttpResponse('设置session成功')

def get_session(request):
    '''获取session'''
    username = request.session['username']
    sex = request.session['sex']

    print(username, sex)

    return HttpResponse('获取session')