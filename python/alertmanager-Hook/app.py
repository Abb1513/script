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
import time

import logging



url = {
    "ops": "",
    "ft":  "",
    "mt":  ""
}



app = Flask(__name__)
handler = logging.FileHandler('flask.log', encoding='utf8')
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)

@app.route("/", methods=["post"])
def send():
    data = request.json
    alerts = data['alerts']
    send = Send_dingding()
    app.logger.info("收到回调")
    try:
        for i in alerts:
            alertname = i["labels"]["alertname"]
            status = i["status"]
            host = i['labels']['instance']
            description = i['annotations']['description']
            summary = i["annotations"]["summary"]
            startTime = time.strptime(i["startsAt"],"%Y-%m-%d %H:%M:%S")
            service_name = i["labels"].get("service_name")
            department = i["labels"].get("department")
            # if status == "resolved":
            #     endTime =  time.strptime(i["endsAt"],"%Y-%m-%d %H:%M:%S")
            if service_name:
                test = """### 测试监控报警: {summary} \n - 状态: **{status}** \n - 服务名称: {service_name} \n - 主机(端口): {host}\n  - 开始时间:{startTime} \n - 详细信息 : {msg}\n  """.format(
                                    status=status, host=host, msg=description, type=alertname, summary = summary, startTime = startTime, service_name = service_name
                        )
            else:
                test = """### 测试监控报警: {summary} \n - 状态: **{status}** \n - 主机(端口): {host}\n  - 开始时间: {startTime} \n - 详细信息\n : {msg}  """.format(
                    status=status, host=host, msg=description, type=alertname, summary=summary, startTime=startTime
                )
            res = send.send_to_dingding(alertname, test, url["ops"]) # 默认发送到 ops
            if department: # 判断部门 发往不同
                res = send.send_to_dingding(alertname, test, url.get(department))
            if res['errcode'] == 0: # 判断是否发送成功。
                app.logger.info("钉钉发送成功, 发送消息: %s"%test)
            else:
                app.logger.erroe("钉钉发送失败, 返回值 ====》%s"%res)
    except Exception as e:
        app.logger.error(e)
    return jsonify({'status':200})
if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host="0.0.0.0", port=6666, debug=False)