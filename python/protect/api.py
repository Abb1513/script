#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/22
# @Software:  PyCharm
# @File    : api.py
# @Author  : Abb1513

from flask import Flask
from flask import request,jsonify
from protect import SaltApi
import logging

salt_api = "http://10.0.1.227:8001/"
app = Flask(__name__)
salt = SaltApi(salt_api)

handler = logging.FileHandler('flask.log', encoding='utf8')
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)



#  0|apis-evaluate|apis-evaluate 服务端口监听失败  meg 原样
@app.route('/' ,methods=['POST'])
def execut():
    # post 传入指定参数 回调远程服务器执行 服务拉起
    data = request.json
    app.logger.info("收到回调,params: %s" % data)
    try:
        host = data["host"]
        msg = data["content"].split('|')
        service_type = msg[0]
        service_name = msg[1]
        status = data['status']
        app.logger.info('service_type: %s,  service_name: %s,  status:%s, host:%s'%(service_type, service_name, status, host))
    except Exception as e:
        app.logger.error(e, "传参错误！")
        return jsonify({'status':"错误参数"})
    if service_type == '0' and status != 'ok':
        salt_client = host
        salt_method = 'cmd.run'
        res = salt.check_server(host, service_name)
        if res:
            app.logger.info("%s 服务活的很欢乐"%service_name)
        else:
            salt_params = "/etc/init.d/%s  restart" %service_name
            res = salt.salt_command(salt_client, salt_method, salt_params)
            app.logger.info("服务已经拉起了, 返回值是: %s"%res)
    else:
        app.logger.info("服务类型:%s 或者 status:%s"%(service_type,status))

    return jsonify({'status': 200})



if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=6000, debug=True)

# result1 = salt.salt_command(salt_client, salt_test)
# if result1:
#
#     app.logger.info("调用salt成功，返回结果: %s"%result1)
#     app.logger.info("%s服务确认死掉了: %s"%(service_name,result1))
# else:
#     app.logger.error("调用salt失败!")