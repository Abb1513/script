#!  /bin/bash

#原nginx日志存放路径
LOG_PATH=/data/logs/nginx/
#nginx 切割后存放路径
LOG_FILES_DIR=/data/backup/nginx/$(date -d "yesterday" +"%Y")/$(date -d "yesterday" +"%m")

#待切割日志名称集合
LOG_FILES_NAME=($(ls ${LOG_PATH}))

#nginx启动脚本
NGINX_SBIN="/usr/local/nginx/sbin/nginx"

#日志保存时间
SAVE_DAYS=60

#创建存放目录
if [ -d ${LOG_FILES_DIR} ]; then
  echo "本月目录已经生成"
else
  mkdir -p ${LOG_FILES_DIR}
fi
LOG_FILES_NUM=${#LOG_FILES_NAME[@]}

#循环切割日志
for ((i = 0; i < ${LOG_FILES_NUM}; i++)); do
  # echo ${LOG_PATH}${LOG_FILES_NAME[$i]}
  # echo  ${LOG_FILES_DIR}/${LOG_FILES_NAME[i]}_$(date -d "yesterday" +"%Y%m%d")
  mv ${LOG_PATH}${LOG_FILES_NAME[$i]} ${LOG_FILES_DIR}/${LOG_FILES_NAME[i]}_$(date -d "yesterday" +"%Y%m%d")
done
if [ $? -eq 0 ]; then
r  #重载配置，生成日志文件
  ${NGINX_SBIN} -s reload
fi
