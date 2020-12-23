Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

####  init-env 
初始服务器环境变量
env  设置java 程序启动时加载的环境参数

#### init-service

username 用户名称 必须和服务名称一致
    例如  服务名为 idp-qes-api.jar  username 为idp-qes-api

uid 创建用户启动的uid  uid 不可太大     顺序递增  2000起

command 启动的命令
没有定义，则为默认值 详情参考 templates/init 启动脚本

>  默认值
`-Xmx512m -Xms512m -jar  $BASE/$NAME.jar --spring.profiles.active=$ENV >/dev/null 2>&1 &`



Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

         
```bash

# 执行初始化 服务器环境
ansible-playbook main.yaml -e "env=dev" --limit 192.168.1.1 --tag init-env

# 初始哈服务器 
ansible-playbook main.yaml -e "username=idp-qes-api"  -e "uid"=2000 -e "command=idp-qes-api#-Xmx512m -Xms512m -jar  $BASE/$NAME.jar --spring.profiles.active=$ENV >/dev/null 2>&1 &"  --limit 192.168.1.1 --tag init-service
ansible-playbook main.yaml -e "username=idp-qes-api"  -e "uid"=2000"  --limit 192.168.1.1 --tag init-service

```
License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
