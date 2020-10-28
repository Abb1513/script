### etcd 指标采集

#### 第一部分: 找到 etcd 的链接信息(ip,port,证书)
因为kube-apiserver 会和 etcd 通信, 所以可以通过 kube-apiserver 的启动信息查到 etcd 的链接信息.

1. 执行 `kubectl get ep  kubernetes -o yaml` 查看 `subsets` 里面的 IP 列表(就是master 节点的地址).
```
apiVersion: v1
kind: Endpoints
metadata:
    manager: kube-apiserver
  name: kubernetes
  namespace: default
subsets:
- addresses:
  - ip: 10.66.10.26
  - ip: 10.66.10.27
  - ip: 10.66.10.28
  ports:
  - name: https
    port: 6443
    protocol: TCP
```
2. 执行 `ssh` 登陆其中任何一个ip地址.
3. 执行 `systemctl status kube-apiserver` 或者 `service kube-apiserver status`.
```
Redirecting to /bin/systemctl status kube-apiserver.service
● kube-apiserver.service - Kubernetes API Server
   Loaded: loaded (/etc/systemd/system/kube-apiserver.service; enabled; vendor preset: disabled)
   Active: active (running) since 四 2020-07-09 21:08:07 CST; 1 weeks 5 days ago
     Docs: https://github.com/GoogleCloudPlatform/kubernetes
 Main PID: 18045 (kube-apiserver)
    Tasks: 24
   Memory: 862.6M
   CGroup: /system.slice/kube-apiserver.service
           └─18045 /opt/k8s/bin/kube-apiserver --advertise-address=10.66.10.26 --default-not-ready-toleration-seconds=360 --default-unreachable-toleration-seconds=360 --feature-gates=DynamicAuditing=true --max-mutating-requests-inflight=2000 --max-reques...
...

```
3. 找到 kube-apiserver 的启动配置文件路径, 示例中为:`/etc/systemd/system/kube-apiserver.service`.

4. 查看配置文件,找到 etcd 的访问端点和证书路径, 例如:`cat /etc/systemd/system/kube-apiserver.service`.
```
[Unit]
Description=Kubernetes API Server
Documentation=https://github.com/GoogleCloudPlatform/kubernetes
After=network.target

[Service]
WorkingDirectory=/data/k8s/k8s/kube-apiserver
ExecStart=/opt/k8s/bin/kube-apiserver \
  ...
  --encryption-provider-config=/etc/kubernetes/encryption-config.yaml \
  --etcd-cafile=/etc/kubernetes/cert/ca.pem \
  --etcd-certfile=/etc/kubernetes/cert/kubernetes.pem \
  --etcd-keyfile=/etc/kubernetes/cert/kubernetes-key.pem \
  --etcd-servers=https://10.66.10.26:2379,https://10.66.10.27:2379,https://10.66.10.28:2379 \
  --bind-address=10.66.10.26 \
  --secure-port=6443 
  ...
```

####  第二部分: 在集群内添加 etcd 的访问端点
5. 在 kube-system 命名空间下创建 Service,Endpoint, 替换示例中的 ip 地址
```
### etcd.yaml

apiVersion: v1
kind: Endpoints
metadata:
  labels:
    kube-app: etcd
  name: kube-etcd
  namespace: kube-system
subsets:
- addresses:
 ### 替换ip, 自行删减
  - ip: 10.66.10.26
  - ip: 10.66.10.27
  - ip: 10.66.10.28
  ports:
  - name: metrics
    port: 2379
    protocol: TCP
---
### name 和 namespace 不要改变, 后面配置 job 的时候需要制定, 如果需要变动, 同时修改job 的过滤规则。
apiVersion: v1
kind: Service
metadata:
  name: kube-etcd
  namespace: kube-system
  labels:
    kube-app: etcd
spec:
  type: ClusterIP
  clusterIP: None
  ports:
  - name: metrics
    port: 2379
    protocol: TCP
```
6. 执行`kubectl apply -f etcd.yaml` 为 etcd 创建集群内访问端点。
7. 把 etcd 证书添加到 secret 里面, 方便prometheus server 使用.
```
### 注意:
### 1. 执行此命令前需要确保命令节点的路径下存在证书配置
### 2. namespace 需要和 prometheus-server 在同一个 namespace 下, 按需修改
### 3. secret name 如果需要变动, 在 prometheus-server 挂载 secret 时也需要同时变更
### 4. 有些证书不是 .pem 而是 .crt, 按需动态调整

kubectl -n kubestar-monitor create secret generic kube-etcd-certs --from-file=/etc/kubernetes/cert/ca.pem --from-file=/etc/kubernetes/cert/kubernetes.pem --from-file=/etc/kubernetes/cert/kubernetes-key.pem
secret/kube-etcd-certs created
```
#### 第三部分: 为 prometheus-server 挂载 etcd 证书并配置 etcd job
8. 执行 `kubectl edit statefulset prometheus-server -n kubestar-monitor` 编辑 prometheus-server
9. 修改的配置文件, 并确保`prometheus-server` 的pod 运行成功
```
        volumeMounts:
        - mountPath: /etc/config
          name: cm-prometheus-config
          readOnly: true
        - mountPath: /etc/prometheus/kube-etcd-certs
          name: secret-kube-etcd-certs
          readOnly: true
      ....
      volumes:
      ...
      - name: secret-kube-etcd-certs
        secret:
          defaultMode: 420
          secretName: kube-etcd-certs
```
10. 到 prometheus 主配置文件配置 etcd job
```
     # kube-etcd 监控
    - job_name: kube-etcd
      honor_labels: false
      kubernetes_sd_configs:
      - role: endpoints
        namespaces:
          names:
          - kube-system
      scheme: https
      tls_config:
        ca_file: /etc/prometheus/kube-etcd-certs/ca.pem
        cert_file: /etc/prometheus/kube-etcd-certs/kubernetes.pem
        key_file: /etc/prometheus/kube-etcd-certs/kubernetes-key.pem
      relabel_configs:
      - source_labels:
        - __meta_kubernetes_endpoints_name
        regex: kube-etcd
        action: keep
```
11. 进入 prometheus 的 Target 页面查看 job 是否已经是 up 状态。
12. etcd 指标采集完成。
