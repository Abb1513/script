# monitor
一站式监控说明

此文档为监控的配置, 部署文档, 监控系统包括:
1. 趋势监控: Prometheus
2. 实时监控: Netdata

#### 趋势监控: Prometheus
##### 配置标准化及原则
1. metric 不得包含含义相似或者一致的 label, 如果存在则应该使用 relabel_configs 保留其中一条 label, 避免过多且无意义的 label 浪费存储资源且不优雅
2. 节点标识仅使用 node, 不得包含含义相似或者一致的 label, 比如 node_name, kubernetes_node 等
3. pod 标识仅使用: pod, 不得包含含义相似或者一致的 label, 比如: kubernetes_pod_name
4. container 标识仅使用: container, 不得包含含义相似或者一致的 label, 比如: kubernetes_container_name
5. namespace 标识仅使用: namespace, 不得包含含义相似或者一致的 label, 比如: kubernetes_namespace
6. job 名字统一, 不得变更
    1. node-exporter
    2. standard-cadvisor
    3. cadvisor
    4. kubelet
    5. kube-state-metrics
    6. kube-dns(备注:即使是coredns 也使用此名字)
    7. kube-apiserver
    8. kube-controller-manager
    9. kube-schduler
    10. kube-etcd
7. job 不得越权采集其他 job 的任务指标, 否则可能导致指标重复,且边界模糊
8. 默认情况下, prometheus 监控部署在 `monitor` 命名空间下
9. 此配置仅部署 prometheus server 及其采集端点, 并不会部署 grafana 等视图应用
10. 此监控的 rbac 配置(例如: `ServiceAccount`,`ClusterRole`,`ClusterRoleBinding` 均会添加额外标识: `kubestar`,避免和现有集群中配置复用和冲突导致误删, 请放心使用)
11. 采集端点需要额外部署时, 必须指定 requeset, limit(当前为最小资源配额原则)。 

| 组件|部署方式| request | limit | 汇总|
|--| --| --|-- | --|
| node-exporter | DaemonSet | cpu/memory = 100m/200Mi | cpu/memory = 100m/200Mi | 100m/200Mi x n |
| standard-cadvisor | DaemonSet | cpu/memory = 100m/200Mi | cpu/memory = 100m/200Mi | 100m/200Mi x n |
| kube-state-metrics | Deployment | cpu/memory = 100m/200Mi | cpu/memory = 100m/200Mi | 100m/200Mi x 1 |
| blackbox | Deployment | cpu/memory = 100m/200Mi | cpu/memory = 100m/200Mi | 100m/200Mi x 1 |
| prometheus-server(按需动态调整) | StatefulSet |cpu/memory = 250m/512Mi,1024m/2Gi | cpu/memory = 250m/512Mi,1024m/4Gi | 1274m/4.5G x 1 |
12. 建议所有 PromQL 都指定 jobname 标记数据来源, 避免指标数据来源猜测和重复计算。
13. 执行: `kubectl apply -f ./prometheus/` 一键式部署 prometheus server 及 相关 job。 
14. ⚠️警告: prometheus server 未挂载任何 path 或者 pv , 容器重启, 数据存在丢失的可能, 请确保能否容忍。
15. 如何为服务配置黑盒监控
```
### 黑盒监控最重要的两个变量
###  1. target 探测的地址,格式为: host:port/path  默认值: kubernetes_service_name.kubernetes_namespace:kubernetes_service_annotation_prometheus_io_http_probe_portkubernetes_service_annotation_prometheus_io_http_probe_path
###  2. module 探测模式, 指定探测模式的协议或者方式, 默认值: http_2xx

### 针对 service

annotation:
  prometheus.io/http-probe: "true"
  prometheus.io/http-probe-port: "8080"
  prometheus.io/http-probe-path: "/probe"  
  ### 为probe path 添加 query params, key只能是大小写和数字
  ### 如果 key 等于 target, 则目标访问地址将会被改写成用户填写的。
  ### 如果 key 等于 module , 则目标探测模式将会被用户填写的改写。
  ### 可选,通常情况无需添加
  prometheus.io/http-probe-params-key: value

### 针对 ingress

### module 探测模式, 默认为: http_2xx
### target 探测地址, 默认为: kubernetes_ingress_scheme://addresskubernetes_ingress_path
### 使用 params 可改写。
annotation:
  prometheus.io/http-probe: "true"
  ### 可选,通常情况无需添加
  prometheus.io/http-probe-params-key: value

#### black-exporter
http探测：
    prometheus.io/scrape: 'true'
    prometheus.io/http-probe: 'true'
    prometheus.io/http-probe-port: '8080'
    prometheus.io/http-probe-path: '/healthz'
 
tcp探测：
    prometheus.io/scrape: 'true'
    prometheus.io/tcp-probe: 'true'
    prometheus.io/tcp-probe-port: '80'
```
16. 如何为服务配置白盒监控
```
#### 仅仅针对 service

annotation:
  prometheus.io/http-metric: "true"
  prometheus.io/http-metric-scheme: http
  prometheus.io/http-metric-port: "8080"
  prometheus.io/http-metric-path: /metric
  ### 为metric url 添加query params, key 只能是大小写字母和数字
  ### 可选,通常情况无需添加
  prometheus.io/http-metric-params-key: value


```
##### 监控体系思路
监控主要分为:
> 节点监控
1. 节点物理资源
以 Daemonset 方式部署 node-exporter 采集每个节点的物理资源。
2. cadvisor 
此处分为两部分: 
    1. kubelet 代理的cadvisor 接口(`https://kubernetes.default.svc:443/api/v1/nodes/nodename/proxy/metrics/cadvisor`)采集大多数容器指标。
    2. 额外部署标准版本的 cadvisor 仅采集容器 TCP连接状态(`container_network_tcp_usage_total`)指标。
3. kubelet 
通过kubelet的接口(`https://kubernetes.default.svc:443/api/v1/nodes/nodename/proxy/metrics`)获取kubelet的监控数据
> kubernetes 资源
1. 资源元数据(kube-state-metrics)
以 Deployment 方式部署 kube-state-metrics 然后获取 kubernetes 资源对象的元数据
> kubernetes 组件
1. kube-dns
2. kube-apiserver
3. kube-controller-manager(暂无)
4. kube-schduler(暂无)
5. kube-etcd(暂无)

> 黑盒
1. service
2. ingress
3. kube-dns


##### 监控组件
##### 完整部署
#### 实时监控: Netdata

#### Alertmanager

报警说明

1. alertmanager 需要和 kubestar (管理平台) 部署到同一个 kubernetes 集群
2. 当kubestar 管理多套集群时, 只需要部署一套alertmanager(位置如 1 所说), 确保集群其他集群到管理集群的网络互通。
3. alertmangaer 的内部服务域名为: `alertmanager.monitor`,端口为:`80`
