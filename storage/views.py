from django.shortcuts import  render
from django.http import JsonResponse,QueryDict
from django.core import serializers
from dashboard.k8s import  auth_check,self_requried_login,load_auth_config
from kubernetes import client,config



def secret(request):
    return  render(request,'storage/secret.html')

def secret_api(request):
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == 'GET':
        namespace = request.GET.get('namespace')
        searchKey = request.GET.get('searchKey', None)
        data = []
        try:
            for secret in core_api.list_namespaced_secret(namespace=namespace).items:
                name = secret.metadata.name
                namespace = secret.metadata.namespace
                data_length = ("空" if secret.data is None else len(secret.data))
                create_time = secret.metadata.creation_timestamp

                se = {"name": name, "namespace": namespace, "data_length": data_length, "create_time": create_time}

                if searchKey:
                    if searchKey in name:
                        data.append(se)
                else:
                    data.append(se)

            code = 0
            msg = "获取数据成功"
        except Exception as e:
            code = 1
            status = getattr(e, 'status')
            if status == 403:
                msg = '没有访问权限'
            else:
                msg = '获取数据失败'

        count = len(data)
        if request.GET.get('page'):
            page = int(request.GET.get('page'))
            limit = int(request.GET.get('limit'))
            end = page * limit
            start = end - limit
            data = data[start:end]
        res = {'code': code, 'msg': msg, 'data': data, 'count': count}
        return JsonResponse(res)

    elif request.method == 'DELETE':
        body = QueryDict(request.body)
        name = body.get('name')
        namespace = body.get('namespace')
        try:
            core_api.delete_namespaced_secret(name,namespace)
            code = 0
            msg = "删除成功"
        except Exception as e:
            code = 1
            status = getattr(e, 'status')
            if status == 403:
                msg = '没有访问权限'
            else:
                msg = '删除失败'
        return JsonResponse({'code': code, 'msg': msg})

def cm(request):
    return  render(request,'storage/configmap.html')

def cm_api(request):
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == 'GET':
        namespace = request.GET.get('namespace')
        searchKey = request.GET.get('searchKey', None)
        data = []
        try:
            for cm in core_api.list_namespaced_config_map(namespace=namespace).items:
                name = cm.metadata.name
                namespace = cm.metadata.namespace
                data_length = ("0" if cm.data is None else len(cm.data))
                create_time = cm.metadata.creation_timestamp

                cm = {"name": name, "namespace": namespace, "data_length": data_length, "create_time": create_time}

                if searchKey:
                    if searchKey in name:
                        data.append(cm)
                else:
                    data.append(cm)

            code = 0
            msg = "获取数据成功"
        except Exception as e:
            code = 1
            status = getattr(e, 'status')
            if status == 403:
                msg = '没有访问权限'
            else:
                msg = '获取数据失败'

        count = len(data)
        if request.GET.get('page'):
            page = int(request.GET.get('page'))
            limit = int(request.GET.get('limit'))
            end = page * limit
            start = end - limit
            data = data[start:end]
        res = {'code': code, 'msg': msg, 'data': data, 'count': count}
        return JsonResponse(res)

    elif request.method == 'DELETE':
        body = QueryDict(request.body)
        name = body.get('name')
        namespace = body.get('namespace')
        try:
            core_api.delete_namespaced_config_map(name,namespace)
            code = 0
            msg = "删除成功"
        except Exception as e:
            code = 1
            status = getattr(e, 'status')
            if status == 403:
                msg = '没有访问权限'
            else:
                msg = '删除失败'
        return JsonResponse({'code': code, 'msg': msg})

def pvc(request):
    return  render(request,'storage/pvc.html')

def pvc_api(request):
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == 'GET':
        namespace = request.GET.get('namespace')
        searchKey = request.GET.get('searchKey', None)
        data = []
        try:
            for pvc in core_api.list_namespaced_persistent_volume_claim(namespace=namespace).items:
                name = pvc.metadata.name
                namespace = pvc.metadata.namespace
                labels = pvc.metadata.labels
                storage_class_name = pvc.spec.storage_class_name
                access_modes = pvc.spec.access_modes
                capacity = (pvc.status.capacity if pvc.status.capacity is None else pvc.status.capacity["storage"])
                volume_name = pvc.spec.volume_name
                status = pvc.status.phase
                create_time = pvc.metadata.creation_timestamp

                pvc = {"name": name, "namespace": namespace, "lables": labels,
                       "storage_class_name": storage_class_name, "access_modes": access_modes, "capacity": capacity,
                       "volume_name": volume_name, "status": status, "create_time": create_time}

                if searchKey:
                    if searchKey in name:
                        data.append(pvc)
                else:
                    data.append(pvc)

            code = 0
            msg = "获取数据成功"
        except Exception as e:
            code = 1
            status = getattr(e, 'status')
            if status == 403:
                msg = '没有访问权限'
            else:
                msg = '获取数据失败'

        count = len(data)
        if request.GET.get('page'):
            page = int(request.GET.get('page'))
            limit = int(request.GET.get('limit'))
            end = page * limit
            start = end - limit
            data = data[start:end]
        res = {'code': code, 'msg': msg, 'data': data, 'count': count}
        return JsonResponse(res)

    elif request.method == 'DELETE':
        body = QueryDict(request.body)
        name = body.get('name')
        namespace = body.get('namespace')
        try:
            core_api.delete_namespaced_persistent_volume_claim(name,namespace)
            code = 0
            msg = "删除成功"
        except Exception as e:
            code = 1
            status = getattr(e, 'status')
            if status == 403:
                msg = '没有访问权限'
            else:
                msg = '删除失败'
        return JsonResponse({'code': code, 'msg': msg})