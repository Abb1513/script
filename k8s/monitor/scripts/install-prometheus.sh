#! /bin/bash

# curl -L "http://transfer.console.marshotspot.com/api/agent/scripts/install.sh" | bash

kubectl apply -f http://kubestar.cn-bj.ufileos.com/kubestar-monitoring%2Fprometheus%2F0-namespace.yaml?UCloudPublicKey=88v0ZQouHX3iuvMpXdHOMKhg2ei7Uw4EXYU58aXtdX5P7P7deOmycg%3D%3D&Signature=djPqbTanAn7RUtjZ0jiobmCyKPQ%3D&Expires=1593694061
kubectl apply -f http://kubestar.cn-bj.ufileos.com/kubestar-monitoring%2Fprometheus%2F1-node-exporter.yaml?UCloudPublicKey=88v0ZQouHX3iuvMpXdHOMKhg2ei7Uw4EXYU58aXtdX5P7P7deOmycg%3D%3D&Signature=MnqFvqn9DvKxP4GW7EaFVhbuKRk%3D&Expires=1593694082
kubectl apply -f http://kubestar.cn-bj.ufileos.com/kubestar-monitoring%2Fprometheus%2F2-standard-cadvisor.yaml?UCloudPublicKey=88v0ZQouHX3iuvMpXdHOMKhg2ei7Uw4EXYU58aXtdX5P7P7deOmycg%3D%3D&Signature=eMDAzxjki%2Fk7U3NuN7JECQwTgR0%3D&Expires=1593694103
kubectl apply -f http://kubestar.cn-bj.ufileos.com/kubestar-monitoring%2Fprometheus%2F3-kube-state-metrics.yaml?UCloudPublicKey=88v0ZQouHX3iuvMpXdHOMKhg2ei7Uw4EXYU58aXtdX5P7P7deOmycg%3D%3D&Signature=cxRJbXqyvuoZ8xO5aRJXUp9pEFs%3D&Expires=1593694115
kubectl apply -f http://kubestar.cn-bj.ufileos.com/kubestar-monitoring%2Fprometheus%2F4-blackbox.yaml?UCloudPublicKey=88v0ZQouHX3iuvMpXdHOMKhg2ei7Uw4EXYU58aXtdX5P7P7deOmycg%3D%3D&Signature=WRgFwl6cyqSzDDXgAtAKZYi0Aww%3D&Expires=1593694124
kubectl apply -f http://kubestar.cn-bj.ufileos.com/kubestar-monitoring%2Fprometheus%2F5-prometheus-bc-config-configmap.yaml?UCloudPublicKey=88v0ZQouHX3iuvMpXdHOMKhg2ei7Uw4EXYU58aXtdX5P7P7deOmycg%3D%3D&Signature=pPaR1rR58NU23MEEm3mTBOff1RM%3D&Expires=1593694142
kubectl apply -f http://kubestar.cn-bj.ufileos.com/kubestar-monitoring%2Fprometheus%2F6-prometheus-config-configmap.yaml?UCloudPublicKey=88v0ZQouHX3iuvMpXdHOMKhg2ei7Uw4EXYU58aXtdX5P7P7deOmycg%3D%3D&Signature=QjYAXSoKe%2FTAxSqkFqa2kfwGjpI%3D&Expires=1593694157
kubectl apply -f http://kubestar.cn-bj.ufileos.com/kubestar-monitoring%2Fprometheus%2F7-prometheus-server.yaml?UCloudPublicKey=88v0ZQouHX3iuvMpXdHOMKhg2ei7Uw4EXYU58aXtdX5P7P7deOmycg%3D%3D&Signature=qYeBAT6S72avBqbbE6GjNyp%2Bdos%3D&Expires=1593694164
