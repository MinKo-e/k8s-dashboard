from django.shortcuts import render
from dashboard.k8s import  auth_check,load_auth_config,self_requried_login
from kubernetes import client
from django.http import JsonResponse,QueryDict

# Create your views here.


def pods(request):
    return render(request, 'workload/pods.html')


# namespace接口
def pods_api(request):
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == 'GET':
        data = []
        namespace = request.GET.get('namespace','default')
        searchKey = request.GET.get('searchKey',None)
        print(searchKey)

        try:
            for po in core_api.list_namespaced_pod(namespace).items:
                name = po.metadata.name
                namespace = po.metadata.namespace
                labels = po.metadata.labels
                pod_ip = po.status.pod_ip

                containers = []  # [{},{},{}]
                status = "None"
                # 只为None说明Pod没有创建（不能调度或者正在下载镜像）
                if po.status.container_statuses is None:
                    status = po.status.conditions[-1].reason
                else:
                    for c in po.status.container_statuses:
                        c_name = c.name
                        c_image = c.image

                        # 获取重启次数
                        restart_count = c.restart_count

                        # 获取容器状态
                        c_status = "None"
                        if c.ready is True:
                            c_status = "Running"
                        elif c.ready is False:
                            if c.state.waiting is not None:
                                c_status = c.state.waiting.reason
                            elif c.state.terminated is not None:
                                c_status = c.state.terminated.reason
                            elif c.state.last_state.terminated is not None:
                                c_status = c.last_state.terminated.reason

                        c = {'c_name': c_name, 'c_image': c_image, 'restart_count': restart_count, 'c_status': c_status}
                        containers.append(c)

                create_time = po.metadata.creation_timestamp
                po = {"name": name, "namespace": namespace, "pod_ip": pod_ip,
                      "labels": labels, "containers": containers, "status": status,
                      "create_time": create_time}
                if searchKey:
                    if searchKey in name:
                        data.append(po)
                else:
                    data.append(po)
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
        print(data)
        return JsonResponse(res)

    elif request.method == 'DELETE':
        body = QueryDict(request.body)
        namespace = body.get('namespace','default')
        name = body.get('name')
        try:
            core_api.delete_namespaced_pod(name,namespace)
            code = 0
            msg = "删除成功"
        except Exception as e:
            code = 1
            status = getattr(e, 'status')
            if status == 403:
                msg = '没有访问权限'
            else:
                msg = '删除失败'
        return  JsonResponse({'code':code,'msg':msg})

def ds(request):
    return render(request, 'workload/daemonset.html')


# namespace接口
def ds_api(request):
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    load_auth_config(auth_type, token)
    apps_api = client.AppsV1Api()
    if request.method == 'GET':
        data = []
        namespace = request.GET.get('namespace','default')
        searchKey = request.GET.get('searchKey',None)
        print(searchKey)

        try:
            for ds in apps_api.list_namespaced_daemon_set(namespace).items:
                name = ds.metadata.name
                namespace = ds.metadata.namespace
                desired_number = ds.status.desired_number_scheduled
                available_number = ds.status.number_available
                labels = ds.metadata.labels
                selector = ds.spec.selector.match_labels
                containers = {}
                for c in ds.spec.template.spec.containers:
                    containers[c.name] = c.image
                create_time = ds.metadata.creation_timestamp

                ds = {"name": name, "namespace": namespace, "labels": labels, "desired_number": desired_number,
                      "available_number": available_number,
                      "selector": selector, "containers": containers, "create_time": create_time}

                if searchKey:
                    if searchKey in name:
                        data.append(ds)
                else:
                    data.append(ds)
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
        print(data)
        return JsonResponse(res)

    elif request.method == 'DELETE':
        body = QueryDict(request.body)
        namespace = body.get('namespace','default')
        name = body.get('name')
        print(namespace)
        try:
            apps_api.delete_namespaced_daemon_set(name,namespace)
            code = 0
            msg = "删除成功"
        except Exception as e:
            code = 1
            status = getattr(e, 'status')
            if status == 403:
                msg = '没有访问权限'
            else:
                msg = '删除失败'
        return  JsonResponse({'code':code,'msg':msg})


def sts(request):
    return render(request, 'workload/statefulset.html')


# namespace接口
def sts_api(request):
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    load_auth_config(auth_type, token)
    apps_api = client.AppsV1Api()
    if request.method == 'GET':
        data = []
        namespace = request.GET.get('namespace','default')
        searchKey = request.GET.get('searchKey',None)
        print(searchKey)

        try:
            for sts in apps_api.list_namespaced_stateful_set(namespace).items:
                name = sts.metadata.name
                namespace = sts.metadata.namespace
                labels = sts.metadata.labels
                selector = sts.spec.selector.match_labels
                replicas = sts.spec.replicas
                ready_replicas = ("0" if sts.status.ready_replicas is None else sts.status.ready_replicas)
                # current_replicas = sts.status.current_replicas
                service_name = sts.spec.service_name
                containers = {}
                for c in sts.spec.template.spec.containers:
                    containers[c.name] = c.image
                create_time =  sts.metadata.creation_timestamp

                sts = {"name": name, "namespace": namespace, "labels": labels, "replicas": replicas,
                      "ready_replicas": ready_replicas, "service_name": service_name,
                      "selector": selector, "containers": containers, "create_time": create_time}

                if searchKey:
                    if searchKey in name:
                        data.append(sts)
                else:
                    data.append(sts)
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
        print(data)
        return JsonResponse(res)

    elif request.method == 'DELETE':
        body = QueryDict(request.body)
        namespace = body.get('namespace','default')
        name = body.get('name')
        print(namespace)
        try:
            apps_api.delete_namespaced_stateful_set(name,namespace)
            code = 0
            msg = "删除成功"
        except Exception as e:
            code = 1
            status = getattr(e, 'status')
            if status == 403:
                msg = '没有访问权限'
            else:
                msg = '删除失败'
        return  JsonResponse({'code':code,'msg':msg})



def deploy(request):
    return render(request, 'workload/deployment.html')


# namespace接口
def deploy_api(request):
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    load_auth_config(auth_type, token)
    apps_api = client.AppsV1Api()
    if request.method == 'GET':
        data = []
        namespace = request.GET.get('namespace','default')
        searchKey = request.GET.get('searchKey',None)
        print(searchKey)

        try:
            for dp in apps_api.list_namespaced_deployment(namespace).items:
                name = dp.metadata.name
                namespace = dp.metadata.namespace
                replicas = dp.spec.replicas
                available_replicas = (0 if dp.status.available_replicas is None else dp.status.available_replicas)
                labels = dp.metadata.labels
                selector = dp.spec.selector.match_labels
                containers = {}
                for c in dp.spec.template.spec.containers:
                    containers[c.name] = c.image
                create_time = dp.metadata.creation_timestamp
                dp = {"name": name, "namespace": namespace, "replicas": replicas,
                      "available_replicas": available_replicas, "labels": labels, "selector": selector,
                      "containers": containers, "create_time": create_time}

                if searchKey:
                    if searchKey in name:
                        data.append(dp)
                else:
                    data.append(dp)
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
        print(data)
        return JsonResponse(res)

    elif request.method == 'DELETE':
        body = QueryDict(request.body)
        namespace = body.get('namespace','default')
        name = body.get('name')
        print(namespace)
        try:
            apps_api.delete_namespaced_deployment(name,namespace)
            code = 0
            msg = "删除成功"
        except Exception as e:
            code = 1
            status = getattr(e, 'status')
            if status == 403:
                msg = '没有访问权限'
            else:
                msg = '删除失败'
        return  JsonResponse({'code':code,'msg':msg})