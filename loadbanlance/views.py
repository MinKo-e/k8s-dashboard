from dashboard.k8s import  load_auth_config,self_requried_login,auth_check
from kubernetes import client,config
from django.shortcuts import  render
from django.http import JsonResponse,QueryDict
from django.core import serializers


def ingress(request):
    return  render(request,'loadbance/ingress.html')

def ingress_api(request):
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    load_auth_config(auth_type, token)
    networking_api = client.NetworkingV1Api()
    if request.method == 'GET':
        namespace = request.GET.get('namespace')
        searchKey = request.GET.get('searchKey', None)
        print(searchKey)
        data = []
        try:
            for ing in networking_api.list_namespaced_ingress(namespace=namespace).items:
                name = ing.metadata.name
                namespace = ing.metadata.namespace
                labels = ing.metadata.labels
                service = "None"
                http_hosts = "None"
                for h in ing.spec.rules:
                    host = h.host
                    path = ("/" if h.http.paths[0].path is None else h.http.paths[0].path)
                    service_name = h.http.paths[0].backend.service.name
                    service_port = str(h.http.paths[0].backend.service.port)
                    http_hosts = {'host': host, 'path': path, 'service_name': service_name,
                                  'service_port': service_port}

                https_hosts = "None"
                if ing.spec.tls is None:
                    https_hosts = ing.spec.tls
                else:
                    for tls in ing.spec.tls:
                        host = tls.hosts[0]
                        secret_name = tls.secret_name
                        https_hosts = {'host': host, 'secret_name': secret_name}

                create_time = ing.metadata.creation_timestamp

                ing = {"name": name, "namespace": namespace, "labels": labels, "http_hosts": http_hosts,
                       "https_hosts": https_hosts, "service": service, "create_time": create_time}

                if searchKey:
                    if searchKey in name:
                        data.append(ing)
                else:
                    data.append(ing)

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
            networking_api.delete_namespaced_ingress(name,namespace)
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


def svc(request):
    return  render(request,'loadbance/service.html')

def svc_api(request):
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == 'GET':
        namespace = request.GET.get('namespace')
        searchKey = request.GET.get('searchKey', None)
        print(searchKey)
        data = []
        try:
            for svc in core_api.list_namespaced_service(namespace=namespace).items:
                name = svc.metadata.name
                labels = svc.metadata.labels
                type = svc.spec.type
                cluster_ip = svc.spec.cluster_ip
                ports = []
                for p in svc.spec.ports:  # 不是序列，不能直接返回
                    port_name = p.name
                    port = p.port
                    target_port = p.target_port
                    protocol = p.protocol
                    node_port = ""
                    if type == "NodePort":
                        node_port = " <br> NodePort: %s" % p.node_port

                    port = {'port_name': port_name, 'port': port, 'protocol': protocol, 'target_port': target_port,
                            'node_port': node_port}
                    ports.append(port)

                selector = svc.spec.selector
                create_time = svc.metadata.creation_timestamp

                # 确认是否关联Pod
                endpoint = ""
                for ep in core_api.list_namespaced_endpoints(namespace=namespace).items:
                    if ep.metadata.name == name and ep.subsets is None:
                        endpoint = "未关联"
                    else:
                        endpoint = "已关联"

                svc = {"name": name, "namespace": namespace, "type": type,
                       "cluster_ip": cluster_ip, "ports": ports, "labels": labels,
                       "selector": selector, "endpoint": endpoint, "create_time": create_time}
                if searchKey:
                    if searchKey in name:
                        data.append(svc)
                else:
                    data.append(svc)

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
            core_api.delete_namespaced_service(name,namespace)
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