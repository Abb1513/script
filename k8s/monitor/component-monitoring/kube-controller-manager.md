### kube-controller-manager
####  第一部分: 找到 kube-controller-manager 的链接信息

默认情况下, 10252 为非加密端口。
1. 到 master 节点组执行 `systemctl status kube-controller-manager` 找到暴露端口
```
[root@k8s-m-1 ~]# systemctl status kube-controller-manager
● kube-controller-manager.service - Kubernetes Controller Manager
   Loaded: loaded (/etc/systemd/system/kube-controller-manager.service; enabled; vendor preset: disabled)
   Active: active (running) since 四 2020-07-09 20:59:01 CST; 1 weeks 6 days ago
     Docs: https://github.com/GoogleCloudPlatform/kubernetes
    ...
```
2. 找到 kube-controller-manager 的启动配置文件路径, 示例中为:`/etc/systemd/system/kube-controller-manager.service`

3. 查看配置文件, 找到 kube-controller-manager 暴露的端口
```
[root@k8s-m-1 ~]# cat /etc/systemd/system/kube-controller-manager.service
[Unit]
Description=Kubernetes Controller Manager
Documentation=https://github.com/GoogleCloudPlatform/kubernetes

[Service]
WorkingDirectory=/data/k8s/k8s/kube-controller-manager
ExecStart=/opt/k8s/bin/kube-controller-manager \
  ...
  --secure-port=10252 \
  --tls-cert-file=/etc/kubernetes/cert/kube-controller-manager.pem \
  --tls-private-key-file=/etc/kubernetes/cert/kube-controller-manager-key.pem \
  ...
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target

# 找到了端口 10252
```

#### 第二部分: 在集群内添加 kube-controller-manager 的访问端点
4. 在 kube-system 命名空间下创建 Service,Endpoint, 替换示例中的 ip 地址
```
### kube-controller-manager.yaml

apiVersion: v1
kind: Endpoints
metadata:
  labels:
    kube-app: kube-controller-manager
  name: kube-controller-manager
  namespace: kube-system
subsets:
- addresses:
 ### 替换ip, 自行删减
  - ip: 10.66.10.26
  - ip: 10.66.10.27
  - ip: 10.66.10.28
  ports:
  - name: metrics
    port: 10252
    protocol: TCP
---
### name 和 namespace 不要改变, 后面配置 job 的时候需要制定, 如果需要变动, 同时修改job 的过滤规则。
apiVersion: v1
kind: Service
metadata:
  name: kube-controller-manager
  namespace: kube-system
  labels:
    kube-app: kube-controller-manager
spec:
  type: ClusterIP
  clusterIP: None
  ports:
  - name: metrics
    port: 10252
    protocol: TCP
```
5. 执行`kubectl apply -f kube-controller-manager.yaml`,为 kube-controller-manager 创建集群内访问端点

#### 第三部分: 为 prometheus-server 配置 kube-controller-manager job
6. 到 prometheus 主配置文件配置 kube-controller-manager job
```
    - job_name: kube-controller-manager
      honor_labels: false
      kubernetes_sd_configs:
      - role: endpoints
        namespaces:
          names:
          - kube-system
      relabel_configs:
      - source_labels:
        - __meta_kubernetes_endpoints_name
        regex: kube-controller-manager
        action: keep
```
7. 
8. kube-controller-manager 指标采集完成。

#### 第四部分: 注意事项和常见问题排查
9. 当知道 kube-controller-manager 的 host 和端口后, 使用 `curl -v host:port/metric` 查看返回数据是否符合prometheus 的指标格式。
10. 当 job 采集出现: `HTTP/1.0 400 Bad Request`,通常是端口问题,请检查端口是否正常。
```
link: https://github.com/opsnull/follow-me-install-kubernetes-cluster/issues/492
```