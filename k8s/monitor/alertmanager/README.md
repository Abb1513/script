# Alertmanager

报警说明

1. alertmanager 需要和 kubestar (管理平台) 部署到同一个 kubernetes 集群
2. 当kubestar 管理多套集群时, 只需要部署一套alertmanager(位置如 1 所说), 确保集群其他集群到管理集群的网络互通。
3. alertmangaer 的内部服务域名为: `alertmanager.kubestar-monitor`,端口为:`80`