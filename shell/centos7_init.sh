#!/bin/bash
# author wangcq

ntp_server=ntp.aliyun.com  
ssh_port=22
ansible_key=http://
defult_user=ops
MASTER="salt.prod" # salt-master

# yum源配置
yum install -y wget 
mv /etc/yum.repos.d/CentOS-Base.repo  /etc/yum.repos.d/CentOS-Base.repo.backup 
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum clean all
yum makecache
yum install -y epel-release

# 常用软件安装
yum install -y ntp wget tree telnet sysstat sysstat iptraf ncurses-devel openssl-devel zlib-devel  nmap screen vim
yum install epel-release  bash-completion   -y



# 设置字符集 utf-8
localectl set-locale LANG=en_US.utf8

# shell 路径显示方式更改
# echo 'export PS1="[ \033[01;33m\u\033[0;36m@\033[01;34m\h \033[01;31m\w\033[0m ]\033[0m \n#"' >> /etc/profile
# source /etc/profile

# sysctl调整
cat >> /etc/sysctl.conf << EOF
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 10000 65000
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_tw_buckets = 36000
net.ipv4.tcp_max_syn_backlog = 16384
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_fin_timeout = 30
vm.swappiness=10
vm.max_map_count = 262144
EOF
sysctl -p

# 文件描述符
cat >> /etc/security/limits.conf << EOF
* soft nofile 65535
* hard nofile 65535
EOF

# 系统用户初始化
useradd ${defult_user} -u 2019
echo '${defult_user}' | passwd --stdin hwb && history -c 
#set sudo authority
echo "" >> /etc/sudoers
echo "#set sudo authority" >> /etc/sudoers
echo "${defult_user} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


# SSH 修改
# 禁止Root远程登录
# 关闭DNS解析
# 不允许空密码
# 修改SSH默认端口
# 关闭GSSAPI校验

\cp /etc/ssh/sshd_config /etc/ssh/sshd_config.`date +%F`
sed -i 's/^GSSAPIAuthentication yes$/GSSAPIAuthentication no/' /etc/ssh/sshd_config
sed -i 's/#UseDNS yes/UseDNS no/' /etc/ssh/sshd_config
sed -i 's%#PermitRootLogin yes%PermitRootLogin no%g' /etc/ssh/sshd_config
sed -i 's%#PermitEmptyPasswords no%PermitEmptyPasswords no%g' /etc/ssh/sshd_config
#sed -i 's%#Port 22%Port ${ssh_port}%g' /etc/ssh/sshd_config

# 时间同步
echo "* 4 * * * /usr/sbin/ntpdate ${ntp_server}> /dev/null 2>&1" >> /var/spool/cron/root

# seliunx 
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config

# ansible 公钥配置

wget ${ansible_key}-O /tmp/ansible_key
cat /tmp/ansible_key >> /home/root/.ssh/authorized_keys
rm -f /tmp/ansible_key
# salt 安装
yum install -y salt-minion
IP=`ifconfig eth0 | grep "inet" | awk '{ print $2}'`

echo "id: ${IP}" >> /etc/salt/minion
echo "master: ${MASTER}" >> /etc/salt/minion
systemctl start salt-minion
systemctl enable salt-minion