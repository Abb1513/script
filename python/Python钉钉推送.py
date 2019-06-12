
# 参考文档 
# https://open-doc.dingtalk.com/microapp/serverapi2/isu6nk

url = ''
msg_text = {"msgtype": "text",
            "text": {
                 "content": "Py 钉钉群组测试消息"
            }
      }
msg_text = json.dumps(msg_text)
head = {
    "Content-Type": "application/json"
}
res = requests.post(url, msg_text, headers=head)

print(json.loads(res.text))