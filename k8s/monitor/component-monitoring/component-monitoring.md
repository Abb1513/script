
### kube-proxy


```
### kube-proxy.yaml

apiVersion: v1
kind: Endpoints
metadata:
  labels:
    kube-app: kube-proxy
  name: kube-proxy
  namespace: kube-system
subsets:
- addresses:
 ### 替换ip, 自行删减
  - ip: 10.66.10.31
  - ip: 10.66.10.32
  - ip: 10.66.10.33
  - ip: 10.66.10.34
  - ip: 10.66.10.35
  - ip: 10.66.10.36
  - ip: 10.66.10.37
  - ip: 10.66.10.38
  - ip: 10.66.10.39
  - ip: 10.66.10.40
  ports:
  - name: metrics
    port: 10249
    protocol: TCP
---
### name 和 namespace 不要改变, 后面配置 job 的时候需要制定, 如果需要变动, 同时修改job 的过滤规则。
apiVersion: v1
kind: Service
metadata:
  name: kube-proxy
  namespace: kube-system
  labels:
    kube-app: kube-proxy
spec:
  type: ClusterIP
  clusterIP: None
  ports:
  - name: metrics
    port: 10249
    protocol: TCP
```

```
    - job_name: kube-proxy
      honor_labels: false
      kubernetes_sd_configs:
      - role: endpoints
        namespaces:
          names:
          - kube-system
      relabel_configs:
      - source_labels:
        - __meta_kubernetes_endpoints_name
        regex: kube-proxy
        action: keep
```