
from django.contrib import admin
from django.urls import include
from django.conf.urls import url
from . import views

app_name = 'sysmanage'

urlpatterns = [
    url(r'^index/$',views.index,name = 'index'),
    url ( r'^login/login_check/$', views.login_check, name='login_check' ),
    url ( r'^login/$', views.login, name='login' ),

]
