# -*- coding: utf-8 -*-
# @Time    : 2018/12/6 15:49
# @Author  : wangcq
# @Software: PyCharm

import requests,json,sys

AgentId  = 1000002
Secret = ""
corpid  =  ""
access_token = requests.get("https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(corpid,Secret ))
access_token = access_token.json()["access_token"]
send_message_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s"%access_token

toparty = sys.argv[1]
message = sys.argv[2]
send_message = {
    #"touser":,
    "toparty":toparty,
    "msgtype":"text",
    "agentid":AgentId,
    "text":{
        "content":message,
            },
    "safe":0,
}

requests.post(send_message_url,data=json.dumps(send_message))