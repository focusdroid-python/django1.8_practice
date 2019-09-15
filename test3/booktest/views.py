from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    '''首页'''
    return render(request, 'booktest/index.html')


def showarg(request, num):
    return HttpResponse(num)

def showtwo(request, num):
    return HttpResponse(num)