#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Time ： 2020/10/23 9:52
@Auth ： huangxd-
@Des : 京东签到脚本
@File ：jd_qd.py
@IDE ：PyCharm
@Motto：Another me.
京东每日签到脚本
"""

import datetime
import pytz
import requests
import re
import time

requests.packages.urllib3.disable_warnings()

class JdQd(object):
    def __init__(self):
        # 京东签到地址
        self.base_url = 'http://sfly.vip:8000/JdSigns'
        # wxpusher Token
        self.appToken = ''
        # wxpusher topicId
        self.topicId = ''
        # jd token
        self.token = ''

    def checkin(self):

        params = {"jdcookie": self.token}
        msg = requests.get(url=self.base_url, params=params).text
        print(msg)
        return msg

    # wxpusher推送
    def wxpusher_send(self, msg):
        print("成功," in msg)
        print("失效" in msg)
        tz = pytz.timezone('Asia/Shanghai') #东八区
        t = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).hour
        print(t)
        if ("成功," in msg  or "失效" in msg) and t in (0, 8, 12, 20):
            url = "http://wxpusher.zjiecode.com/api/send/message"
            params = {"appToken": self.appToken, "topicId": self.topicId, "content": "京东签到：\n\n" + msg}
            response = requests.get(url=url, params=params).text
            print(response)

    def main(self):
        msg = self.checkin()
        self.wxpusher_send(msg)

# 云函数入口
def main_handler(event, context):
    run = JdQd()
    run.main()

if __name__ == '__main__':
    run = JdQd()
    run.main()
