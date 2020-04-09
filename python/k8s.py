#!/usr/bin/python2

# @Name    : python
# @Time    : 2020/4/8
# @IDE     : PyCharm
# @Author  : Ops
from kubernetes import client
import argparse
import json

token = """
eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi1vcHMtdG9rZW4tYnMyd2giLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiYWRtaW4tb3BzIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZjRhOWJkOWMtNzk2Ny0xMWVhLWIzZDQtZjA3OTU5NjkyZWE4Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmFkbWluLW9wcyJ9.IQTVstTBY_TvpEnWlNh7i_hym07vNTwvO2w0j4gmEwiIhHgTz_R28pr8QnbITmVucszXTNL6YMEDRAgi2tKu1bwcBXG9aDgBvUnbA2VROM0IhMFusJIyu8aHnKZFucDkLz2La4iX8lRblzkNdDJdbia8eu6lwe-RNzPXaePR-kQvsJfRKfc2zIP1xfnK3tqBcnUzBVSZH5LhEd4WL6IMW_niTm5qGKEO5pSec0enurMnGxR5gxHM0p33S3ucxuDH068lFUE2_lyG7ZJYjiSygfk2awpTzWN_qsCsHnDpiXuDkpB05BsMQqkOjiyS-TT3_Yx1R-G5NoGTxRk1ILhxyw
""".strip('\n')


def getPod():
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        pass
        # print "%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name)


def exportNodeport(servicename, port, env):
    """
    :param servicename: k8s service Name
    :param port:  target port
    :return:  node Port
    """
    api_instance = client.CoreV1Api()
    service = client.V1Service()
    service.api_version = "v1"
    service.kind = "Service"
    service.metadata = client.V1ObjectMeta(name="py-go-" + servicename)
    spec = client.V1ServiceSpec()
    spec.type = 'NodePort'
    spec.selector = {"workload.user.cattle.io/workloadselector": "deployment-qapple-dev01-go-" + servicename}
    spec.ports = [client.V1ServicePort(protocol="TCP", port=int(i), target_port=int(i), name=servicename + i) for i in
                  port[0]]
    # spec.ports = [client.V1ServicePort(protocol="TCP", port=10000, target_port=10000),
    #               client.V1ServicePort(protocol="TCP", port=20000, target_port=20000),
    #               client.V1ServicePort(protocol="TCP", port=30000, target_port=30000, name=)
    #              ]
    service.spec = spec
    # env
    result = api_instance.create_namespaced_service(namespace=env, body=service)
    # print result.spec.ports
    for i in result.spec.ports:
        print "%s: port:%d --> nodeport: 192.168.0.211:%d" % (
            servicename, i.port, i.node_port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="input ServiceName, ServicePort And env")
    parser.add_argument('-n', type=str, required=True,
                        help='input ServiceName')
    parser.add_argument('-p', required=True, type=str, action='append', nargs='+',
                        help='input ServicePort')
    parser.add_argument('-e', required=True, type=str,
                        help='input K8s namespace')
    args = parser.parse_args()
    print type(args.p[0][0])
    conf = client.Configuration()
    conf.host = 'https://192.168.0.211:6443'
    conf.api_key_prefix['authorization'] = 'Bearer'
    conf.api_key = {"authorization": token}
    conf.verify_ssl = False
    client.Configuration.set_default(conf)
    # getPod()
    exportNodeport(args.n, args.p, args.e)
