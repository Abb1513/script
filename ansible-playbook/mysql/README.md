#### 变量
```shell script
修改 defaults main.yml
mysql二进制包提前下载 放在tmp 目录下 
http://mirrors.163.com/mysql/Downloads/MySQL-5.7/mysql-5.7.27-el7-x86_64.tar.gz
其他文件名包, 修改task main下面文件名
```
#### 使用
```shell script
vim main.yml
---
- hosts: 192.168.1.50
  roles:
    - role: mysql

ansible-playbook main.yml
```

#### 目录结构
```shell script
.
├── README.md  # 文档
├── defaults  # 默认变量
├── handlers # 回调
├── meta  
├── tasks # 具体任务
├── templates # 模板文件
├── tests
└── vars # 变量
```

