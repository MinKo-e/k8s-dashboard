from django.urls import path, re_path
from loadbanlance import views



urlpatterns = [
    re_path('^svc/$',views.svc,name='svc'),
    re_path('^svc_api/$',views.svc_api,name='svc_api'),
    re_path('^ingress/$',views.ingress,name='ingress'),
    re_path('^ingress_api/$',views.ingress_api,name='ingress_api'),
]
