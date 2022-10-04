"""k8s URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path,include
from dashboard import views
import wordload.urls
import storage.urls
import loadbanlance.urls
import dashboard.urls
from dashboard import views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('workload/', include('wordload.urls')),
    path('loadbanlance/', include('loadbanlance.urls')),
    path('storage/', include('storage.urls')),
    re_path('^$', views.index),
    re_path('^login/$', views.login, name='login'),
    re_path('^logout/$', views.logout, name='logout'),
    re_path('^namespace_api/$', views.namespace_api,name='namespace_api'),
    re_path('^namespace/$', views.namespace,name='namespace'),
    re_path('^pv/$',views.pv,name='pv'),
    re_path('^pv_api/$',views.pv_api,name='pv_api'),
    re_path('^node/$', views.node,name='node'),
    re_path('^node_api/$', views.node_api, name='node_api'),





]
