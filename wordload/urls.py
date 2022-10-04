from django.urls import path, re_path
from wordload import views


urlpatterns = [
    re_path('^deploy/$',views.deploy,name='deploy'),
    re_path('^deploy_api/$',views.deploy_api,name='deploy_api'),
    re_path('^ds/$', views.ds, name='ds'),
    re_path('^ds_api/$', views.ds_api, name='ds_api'),
    re_path('^sts/$', views.sts, name='sts'),
    re_path('^sts_api/$', views.sts_api, name='sts_api'),
    re_path('^pods/$', views.pods, name='pods'),
    re_path('^pods_api/$', views.pods_api, name='pods_api'),

]
