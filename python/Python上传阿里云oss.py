#!/usr/bin/env python
# encoding:utf-8
import os,  string, oss2

accessKeySecret = ''
endpoint_url = 'http://oss-cn-shenzhen.aliyuncs.com'
accessKeyID = ''


access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', accessKeyID)
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', accessKeySecret)
endpoint = os.getenv('OSS_TEST_ENDPOINT', endpoint_url)
bucket_name = os.getenv('OSS_TEST_BUCKET', 'dbs-backup-1418643921234586-cn-shenzhen')


# 检测参数， 不存在抛出异常
for param in (access_key_id, access_key_secret, bucket_name, endpoint):
    assert '<' not in param, '请设置参数：' + param

# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
#/data/bakup/
up_pwd = ['confluence/','gitlab/']

for i in up_pwd:
    path = '/data/bakup/' + i
    file_list = os.listdir(path)
    for v in file_list:
        file_path = path + v
       # print file_path, path, i , v
        oss2.resumable_upload(bucket, '{}{}'.format(i,v), filename=file_path)
       # print file_path, path, i , v
        os.remove(file_path)
        # oss2 实例化对象， 远程上传后的文件名，  本地待上传文件名
