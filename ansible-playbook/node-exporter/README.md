#### 变量
```shell script
修改 defaults main.yml
二进制包放在 files下面
替换包 修改defaults main.yml file_name字段
```
#### 使用
```shell script
vim main.yml
---
- hosts: 192.168.1.50
  roles:
    - role: node-exporter

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

