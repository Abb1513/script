#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26
# @Software:  PyCharm
# @File    : app.py
# @Author  : Abb1513
# Prometheus 钉钉告警组件


from flask import Flask
from flask import request,jsonify
from dingding import *

import logging


app = Flask(__name__)
handler = logging.FileHandler('flask.log', encoding='utf8')
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.info("收到回调")

@app.route("/", methods=["post"])
def send():
    data = request.json
    alertname = data['groupLabels']['alertname']
    status = data['status']
    alerts = data['alerts']
    send = Send_dingding()
    app.logger.info("收到回调")
    try:
        for i in alerts:
            host = i['labels']['instance']
            msg = i['annotations']['description']
            test = """### Ops 网络报警 {type} \n #### status: *{status}* \n host: {host}  \n message: {msg}""".format(status=status, host=host, msg=msg, type=alertname)
            if send.time_is():
                res = send.send_to_dingding(alertname, test)
                print(res['errcode'])
                if res['errcode'] == 0:
                    app.logger.info("钉钉发送成功, 发送消息: %s"%test)
                else:
                    app.logger.erroe("钉钉发送失败, 返回值 ====》%s"%res)
    except Exception as e:
        app.logger.error(e)
    return jsonify({'status': 200,"data":data})


    return jsonify({'status':200})
if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=6666, debug=True)