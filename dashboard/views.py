import os.path, hashlib, random
from kubernetes import client
from dashboard.k8s import self_requried_login, auth_check, load_auth_config
from django.shortcuts import render, redirect
from django.http import JsonResponse,QueryDict


# @self_requried_login
def index(request):
    return render(request, 'index.html')


def logout(request):
    if request.session.get('auth_type') == 'kubeconfig':
        print(request.session.get('auth_type'))
        print(request.session.get('token'))
        file = request.session.get('token')
        print(os.path.join(os.path.dirname(__file__)), f'kubeconfig\\{file}')
        os.remove(file)
    request.session.flush()
    return redirect('/login')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', )
    elif request.method == 'POST':
        token = request.POST.get('token')
        if token:
            res = auth_check('token', token)
            if res:
                request.session['auth_type'] = 'token'
                request.session['is_login'] = True
                request.session['token'] = token
                print(request.session['auth_type'], request.session['is_login'], request.session['token'])
                code = 0
                msg = '验证通过'
            else:
                code = 1
                msg = '验证失败'
        else:
            print(request.FILES)
            print(request.POST)
            file = request.FILES.get('file')
            token = hashlib.md5(str(random.random()).encode()).hexdigest()
            file_path = os.path.join('kubeconfig', token)
            with open(file_path, 'w') as w:
                data = file.read().decode()
                w.write(data)
            res = auth_check('config', file_path)
            if res:
                code = 0
                msg = '验证通过'
                request.session['auth_type'] = 'kubeconfig'
                request.session['is_login'] = True
                request.session['token'] = file_path
                print(request.session)
            else:
                code = 1
                msg = '验证失败'
        res = {'code': code, 'msg': msg}
        return JsonResponse(res)

def node(request):
    return render(request, 'dashboard/node.html')


# namespace接口
def node_api(request):
    auth_type = request.session.get('auth_type')

    token = request.session.get('token')
    load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == 'GET':
        data = []
        searchKey = request.GET.get('searchKey',None)
        try:
            for node in core_api.list_node_with_http_info()[0].items:
                name = node.metadata.name
                labels = node.metadata.labels
                status = node.status.conditions[-1].status
                scheduler = ("是" if node.spec.unschedulable is None else "否")
                cpu = node.status.capacity['cpu']
                taints = node.spec.taints
                memory = str(node.status.capacity['memory'])
                fmt = memory.split('Ki')
                memory = str(int(int(fmt[0]) / 1024))  + 'Mi'

                kebelet_version = node.status.node_info.kubelet_version
                cri_version = node.status.node_info.container_runtime_version
                create_time = node.metadata.creation_timestamp
                node = {"name": name, "labels": labels, "status": status,
                        "scheduler": scheduler, "cpu": cpu, "memory": memory,
                        "kebelet_version": kebelet_version, "cri_version": cri_version,
                        "create_time": create_time,'taints':taints}

                if searchKey:
                    if searchKey in name:
                        data.append(node)
                else:
                    data.append(node)
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
        try:
            core_api.delete_namespace(body.get('name'))
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

def namespace(request):
    return render(request, 'dashboard/namespace.html')


# namespace接口
def namespace_api(request):
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == 'GET':

        data = []
        searchKey = request.GET.get('searchKey',None)

        try:
            for ns in core_api.list_namespace().items:
                name = ns.metadata.name
                labels = ns.metadata.labels
                create_time = ns.metadata.creation_timestamp
                namespace = {'name': name, 'labels': labels, 'create_time': create_time}

                if searchKey:
                    print('search')
                    print(type(name))
                    if searchKey in name:
                        data.append(namespace)
                else:
                    data.append(namespace)
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
        try:
            core_api.delete_namespace(body.get('name'))
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

def pv(request):
    return  render(request,'dashboard/persistentvolumes.html')

def pv_api(request):
    auth_type = request.session.get('auth_type')
    token = request.session.get('token')
    load_auth_config(auth_type, token)
    core_api = client.CoreV1Api()
    if request.method == 'GET':

        searchKey = request.GET.get('searchKey', None)
        print(searchKey)
        data = []
        try:
            for pv in core_api.list_persistent_volume().items:
                name = pv.metadata.name
                capacity = pv.spec.capacity["storage"]
                access_modes = pv.spec.access_modes
                reclaim_policy = pv.spec.persistent_volume_reclaim_policy
                status = pv.status.phase
                if pv.spec.claim_ref is not None:
                    pvc_ns = pv.spec.claim_ref.namespace
                    pvc_name = pv.spec.claim_ref.name
                    pvc = "%s / %s" % (pvc_ns, pvc_name)
                else:
                    pvc = "未绑定"
                storage_class = pv.spec.storage_class_name
                create_time = pv.metadata.creation_timestamp
                pv = {"name": name, "capacity": capacity, "access_modes": access_modes,
                      "reclaim_policy": reclaim_policy, "status": status, "pvc": pvc,
                      "storage_class": storage_class, "create_time": create_time}
                if searchKey:
                    if searchKey in name:
                        data.append(pv)
                else:
                    data.append(pv)

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
        print(res)
        return JsonResponse(res)

    elif request.method == 'DELETE':
        body = QueryDict(request.body)
        try:
            core_api.delete_persistent_volume(body.get('name'))
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

