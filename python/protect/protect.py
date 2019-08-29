#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/22
# @Software:  PyCharm
# @File    : protect.py
# @Author  : Abb1513



import requests
import json

try:
    import cookielib
except:
    import http.cookiejar as cookielib

# 使用urllib2请求https出错，做的设置
import ssl
context = ssl._create_unverified_context()

# 使用requests请求https出现警告，做的设置
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



salt_api = "http://10.0.1.227:8001/"

class SaltApi:
    """
    定义salt api接口的类
    初始化获得tokens
    """
    def __init__(self, url):
        self.url = url
        self.username = "saltapi"
        self.password = "qaz123"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
            "Content-type": "application/json"
        }
        self.params = {'client': 'local', 'fun': '', 'tgt': ''}
        # self.params = {'client': 'local', 'fun': '', 'tgt': '', 'arg': ''}
        self.login_url = self.url + "login"
        self.login_params = {'username': self.username, 'password': self.password, 'eauth': 'pam'}
        self.token = self.get_data(self.login_url, self.login_params)['token']
        self.headers['X-Auth-Token'] = self.token

    def get_data(self, url, params):
        send_data = json.dumps(params)
        request = requests.post(url, data=send_data, headers=self.headers, verify=False)
        response = request.json()
        result = dict(response)
        # print result
        return result['return'][0]

    def salt_command(self, tgt, method, arg=None):
        """远程执行命令，相当于salt 'client1' cmd.run 'free -m'"""
        #   tgt 目标 机器
        if arg:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'arg': arg, 'expr_form':'ipcidr'}
        else:
            params = {'client': 'local', 'fun': method, 'tgt': tgt, 'expr_form':'ipcidr'}
        result = self.get_data(self.url, params)
        return result

    def check_server(self,host,server_name):
        salt_method = 'cmd.run'
        salt_params = 'ps -uax | grep %s | grep -v grep '%server_name
        res = self.salt_command(host, salt_method, salt_params)
        for _,k in res.items():
            if k:
                return True
        return False



def main():
    salt = SaltApi(salt_api)
    salt_client = '10.0.1.59'
   # salt_test = 'test.ping'
    salt_method = 'cmd.run'
    salt_params = 'ps -uax | grep apis-channel-impl | grep -v grep '
    res = salt.check_server(salt_client, 'apis-channel-impl')
    print(res)
    # result1 = salt.salt_command(salt_client, salt_test)
    # for i in result1.keys():
    #     print (i, ': ', result1[i])
    # result2 = salt.salt_command(salt_client, salt_method, salt_params)
    # for k,v in result2.items():
    #     if v : # 判断是否进程是否存或
    #         print('[+]')
    #     else:
    #         salt_params = '/etc/init.d/apis-channel-impl restart'
    #         result2 = salt.salt_command(salt_client, salt_method, salt_params)
    #         print(result2)

if __name__ == '__main__':
    main()