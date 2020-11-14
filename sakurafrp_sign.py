#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Time ： 2020/10/23 9:52
@Auth ： huangxd-
@Des : sakurafrp每日签到
@File ：sakurafrp_sign.py
@IDE ：PyCharm
@Motto：Another me.
sakurafrp每日签到
"""
import requests
import re

requests.packages.urllib3.disable_warnings()

class Sakurafrp(object):
    def __init__(self):
        # wxpusher Token
        self.appToken = ''
        # wxpusher topicId
        self.topicId = ''

    # wxpusher推送
    def wxpusher_send(self, msg):
        url = "http://wxpusher.zjiecode.com/api/send/message"
        params = {"appToken": self.appToken, "topicId": self.topicId, "content": "sakurafrp每日签到", "url": "https://www.natfrp.com/user/sign"}
        response = requests.get(url=url, params=params).text
        print(response)

    def main(self):
        self.wxpusher_send('')

# 云函数入口
def main_handler(event, context):
    run = Sakurafrp()
    run.main()

if __name__ == '__main__':
    run = SspanelQd()
    run.main()

