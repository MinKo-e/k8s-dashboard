
from django.shortcuts import redirect
from  kubernetes import client,config
import os
def self_requried_login(func):
    def inner(request,*args,**kwargs):

        is_login = request.session['is_login',False]

        if is_login:
            func(request,*args,**kwargs)
        else:
            return  redirect('/login')
    return  inner

def auth_check(auth_type,token):
    if auth_type == 'token':
        configuration = client.Configuration()
        configuration.host = "https://192.168.19.10:6443"  # APISERVER地址
        configuration.ssl_ca_cert = 'ca.crt'  # CA证书
        configuration.verify_ssl = True  # 启用证书验证
        configuration.api_key = {"authorization": "Bearer " + token}  # 指定Token字符串
        client.Configuration.set_default(configuration)
        try:
            core_api = client.CoreApi()
            core_api.get_api_versions()
            return True
        except Exception as e:
            return False
    elif auth_type == 'config':
        config.load_kube_config(token)
        try:
            core_api = client.CoreApi()
            core_api.get_api_versions()
            return True
        except:
            return False


def load_auth_config(auth_type,str):
    if auth_type == 'token':
        token = str
        configuration = client.Configuration()
        configuration.host = "https://192.168.19.10:6443"  # APISERVER地址
        configuration.ssl_ca_cert = r"%s" % (os.path.join('kubeconfig', "ca.crt"))  # CA证书
        configuration.verify_ssl = True  # 启用证书验证
        configuration.api_key = {"authorization": "Bearer " + token}  # 指定Token字符串
        client.Configuration.set_default(configuration)
    elif auth_type == 'kubeconfig':
        random_str = str
        file_path = os.path.join(random_str)
        config.load_kube_config(r"%s" % file_path)
