
#_*_ coding:utf-8 _*_
from django.shortcuts import HttpResponse
from django.contrib import auth
import json
from lib import hashmd5
import time



def auth(func):
    '''
    装饰器，验证用户是否登录
    :param func:
    :return:
    '''
    def wrapper(request, *args, **kwargs):
        if request.session.get("is_login", False):
            current_user = request.session.get("current_user")
            models.Users.objects.filter(id=current_user['id']).update(is_online=True)
            return func(request, *args, **kwargs)
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'error': '需要登录才能操作'}))
    return wrapper



@auth
def get_online_users(request):
    '''
    1、查询当前状态为登录的用户
    2、处理生成表单返回信息
    :param request:
    :return:
    '''
    current_user = request.session.get("current_user")
    user_id = current_user.get("id")

    users = models.Users.objects.exclude(id=user_id ).filter(is_online=True).values("id", "head_picture", "user_name")
    users_list = list(users)
    return HttpResponse(json.dumps({
        'status': 'ok',
        'data': users_list
    }))




def login(request):

    '''
    1.接收数据进行处理
    2.比对接收的密码md5和数据库查询的md5
    3.vmodels.Users.valid字段查询用户是否可用
    :param request:
    :return:
    '''
    if request.method == 'POST':
        ret = {'status': '',
               'error': '',
               'display_name': '',
               'head_pic': ''}
        user_name = request.POST.get ( "user_name" )
        password = request.POST.get ( "password" )
        if user_name and password:
            password_md5 = hashmd5.hashencrypt(password)
            # 查询用户信息
            user = models.Users.objects.filter ( user_name=user_name, password=password_md5 ).first ()
            if user:
                # users.valid 确认用户是否能够有效登录
                if user.valid:
                    # 有效
                    # 将用户信息登记到session中
                    request.session['is_login'] = True
                    request.session['current_user'] = {
                        'id': user.id,
                        'user_name': user.user_name,
                    }

                    # 返回验证通过信息+用户昵称+头像url到客户端
                    ret['status'] = 'ok'
                    #登录状态变为is_online

                    user = models.Users.objects.filter ( user_name=user_name, password=password_md5 ).first ()
                    user.is_online = True
                    user.save()
                else:
                    ret['status'] = 'fail'
                    ret['error'] = '该用户已禁用'
            else:
                ret['status'] = 'fail'
                ret['error'] = '用户名或密码不正确'
        else:
            ret['status'] = 'fail'
            ret['error'] = '用户名或者密码不能为空'
        return HttpResponse ( json.dumps ( ret ) )


@auth
def logout(request):
    '''
    清空会话信息，返回注销成功值
    '''

    user = models.Users.objects.filter ( user_name=request.session.get('current_user')['user_name']).first ()
    user.is_online = False
    user.save ()
    if request.session.get ( 'is_login' ):
        request.session['is_login'] = False
    if  request.session.get('current_user'):
        request.session['current_user'] = {}
    return HttpResponse(json.dumps({'status': 'ok'}))