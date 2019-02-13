from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as syslogin
from back_manage import settings
import json
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse

from django.template import RequestContext


def index(request):
    return render(request,'index.html')

def login(req):
    return render(req,'login.html')


def login_check(req):
    ret = {'status': '',
           'error': '',
           'display_name': ''
           }
    if req.method == 'POST':
        username = req.POST.get('username','')
        password = req.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(req,user)
            req.session['user'] = username
            ret['status'] = 'ok'
            ret['display_name'] = username
            return  HttpResponse(json.dumps ( ret ) )
        else:
            ret['error'] = '用户名或密码错误'
            return  HttpResponse(json.dumps ( ret ) )
