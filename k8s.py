from dashboard.k8s import  auth_check,load_auth_config,config
from kubernetes import client
token = 'cmRXSmxjbTVsZEdWekwzTmxjblpwWTJWaFkyTnZkVzUwSWl3aWEzVmlaWEp1WlhSbGN5NXBieTl6WlhKMmFXTmxZV05qYjNWdWRDOXVZVzFsYzNCaFkyVWlPaUprWldaaGRXeDBJaXdpYTNWaVpYSnVaWFJsY3k1cGJ5OXpaWEoyYVdObFlXTmpiM1Z1ZEM5elpXTnlaWFF1Ym1GdFpTSTZJbUZrYldsdUxYVnpaWEl0ZEc5clpXNHRjRGt5Y2pjaUxDSnJkV0psY201bGRHVnpMbWx2TDNObGNuWnBZMlZoWTJOdmRXNTBMM05sY25acFkyVXRZV05qYjNWdWRDNXVZVzFsSWpvaVlXUnRhVzR0ZFhObGNpSXNJbXQxWW1WeWJtVjBaWE11YVc4dmMyVnlkbWxqWldGalkyOTFiblF2YzJWeWRtbGpaUzFoWTJOdmRXNTBMblZwWkNJNklqZGlNVE5oTjJZNExXWmtZVGN0TkRnNE5pMWlNVFV5TFdKbVlqSXlOakZoT1daaVpDSXNJbk4xWWlJNkluTjVjM1JsYlRwelpYSjJhV05sWVdOamIzVnVkRHBrWldaaGRXeDBPbUZrYldsdUxYVnpaWElpZlEuakZvdEE2NDQwWVUweU4wTDNON1lDV3E1ZjRTbUVqMVVsNmtYdENtTnRfNlFwR2Z0QjYyRGRvbUhfeHloaV9JY3RpMUVUODlleGN2ZUtER1JTLVlxUjhRTnlnT1VpODFLM0psc2dnUmhodERzMTBwQUxhUlJubnJIQ2pid2h3d3phUVVOdDJTS3JYYXA2OWdUbU51dVV2SEoyOXFMdzQydWtaUU4wR2RubFkycnk0cUs3XzlfSDlaMGwxcmJQRC1SVUpDR2NIekxPMmJaQm5WMkRTZDdWemZvVU8yQ0syLVF2TDRqZmVmcV83VjB1NExrRTFIeXg1OFJ5cjBTcV91bzI0TlhkU1lXc1ltZWd0QVJIdjVQZzVLOUxuazE3MTdHa01QR2FfZTVpMTdVaHlQb1d5bTdtaVBpNXktVTN2eFBKUzFwU0U1X0xqZjBMbVNqZ0twTjRB'
del token
token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6InI4cmIzelk1c0RaUDN3YXVfU21QbUpnRU9YUVdNLUtkTnRDY0VCOEZNYXcifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImFkbWluLXVzZXItdG9rZW4tcDkycjciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiYWRtaW4tdXNlciIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjdiMTNhN2Y4LWZkYTctNDg4Ni1iMTUyLWJmYjIyNjFhOWZiZCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmFkbWluLXVzZXIifQ.jFotA6440YU0yN0L3N7YCWq5f4SmEj1Ul6kXtCmNt_6QpGftB62DdomH_xyhi_Icti1ET89excveKDGRS-YqR8QNygOUi81K3JlsggRhhtDs10pALaRRnnrHCjbwhwwzaQUNt2SKrXap69gTmNuuUvHJ29qLw42ukZQN0GdnlY2ry4qK7_9_H9Z0l1rbPD-RUJCGcHzLO2bZBnV2DSd7VzfoUO2CK2-QvL4jfefq_7V0u4LkE1Hyx58Ryr0Sq_uo24NXdSYWsYmegtARHv5Pg5K9Lnk1717GkMPGa_e5i17UhyPoWym7miPi5y-U3vxPJS1pSE5_Ljf0LmSjgKpN4A'
configuration = client.Configuration()
configuration.host = "https://192.168.19.10:6443"  # APISERVER地址
configuration.ssl_ca_cert = 'ca.crt'  # CA证书
configuration.verify_ssl = True  # 启用证书验证
configuration.api_key = {"authorization": "Bearer " + token}  # 指定Token字符串
client.Configuration.set_default(configuration)
core_api = client.NetworkingV1Api()


try:
    for ing in core_api.list_namespaced_ingress(namespace='default').items:
        name = ing.metadata.name
        namespace = ing.metadata.namespace
        labels = ing.metadata.labels
        service = "None"
        http_hosts = "None"
        for h in ing.spec.rules:
            host = h.host
            path = ("/" if h.http.paths[0].path is None else h.http.paths[0].path)
            service_name = h.http.paths[0].backend.service.name
            service_port = h.http.paths[0].backend.service.port
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
        print(ing)

except Exception as e:
    print(e)