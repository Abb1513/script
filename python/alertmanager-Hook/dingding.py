#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/26
# @Software:  PyCharm
# @File    : dingding.py
# @Author  : Abb1513

import requests,json,datetime

class Send_dingding:
    def send_to_dingding(self,title, text):
        """
        :param title:  消息标题
        :param text:  消息内容
        :param url:   钉钉机器人url
        :return:  发送状态
        """
        url = ''
        msg_text = {"msgtype": "markdown",
                    "markdown": {
                        "title": "Ops 网络报警" + title ,
                        "text": text
                        }
                    }
        msg_text = json.dumps(msg_text)
        head = {
            "Content-Type": "application/json"
        }
        res = requests.post(url, msg_text, headers=head)
        return json.loads(res.text)

    def time_is(self):
        d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')
        d_time2 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '21:00', '%Y-%m-%d%H:%M')
        now_time = datetime.datetime.now()
        if  d_time1 < now_time < d_time2:
            return True
        else:
            return False



