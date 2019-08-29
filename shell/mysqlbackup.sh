#!/bin/bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
export PATH
#数据库用户名
dbuser='root'
#数据库用密码
dbpasswd=''
#需要备份的数据库，多个数据库用空格分开
dbname=""
#备份时间
backtime=`date +%Y%m%d%H%M%S`
#mysql安装路径
mysqlpath='/application/mysql/bin'


#判断日志路径
if [ ! -d /data/mysqlbackup/log/ ]; then
  mkdir -p /data/mysqlbackup/log
fi

#判断数据存放路径
if [ ! -d /data/mysqlbackup/data ]; then
  mkdir -p /data/mysqlbackup/data
fi

#日志备份路径
logpath='/data/mysqlbackup/log'
#数据备份路径
datapath='/data/mysqlbackup/data'


#正式备份数据库 取上面变量数组
for DB_name in $dbname; do 

#日志记录头部
echo "备份时间为${backtime},备份数据库 ${DB_name} 开始" >> ${logpath}/mysqllog.log


source=`${mysqlpath}/mysqldump -u${dbuser} -p${dbpasswd} ${DB_name}> ${datapath}/${DB_name}${backtime}.sql` 2>> ${logpath}/mysqllog.log;
#备份成功以下操作
if [ "$?" == 0 ];then
cd $datapath
#为节约硬盘空间，将数据库压缩
tar jcvf ${DB_name}${backtime}.tar.bz2 ${DB_name}${backtime}.sql > /dev/null
#删除原始文件，只留压缩后文件	
rm -f ${datapath}/${DB_name}${backtime}.sql
#删除15天前备份，也就是只保存15天内的备份
find $datapath -name "*.tar.bz2" -type f -mtime +15 -exec rm -rf {} \; > /dev/null 2>&1
echo "数据库表 ${DB_name} 备份成功!!" >> ${logpath}/mysqllog.log
else
#备份失败则进行以下操作
echo "数据库表 ${DB_name} 备份失败!!" >> ${logpath}/mysqllog.log
fi
done
echo $? >${logpath}/mysqlbak.log

echo "======================================" >> ${logpath}/mysqllog.log


