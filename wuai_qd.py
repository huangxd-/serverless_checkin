#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Time ： 2020/11/11 21:08
@Auth ： huangxd-
@Des : 吾爱破解每日签到
@File ：wuaipojie_sign.py
@IDE ：PyCharm
@Motto：Another me.
吾爱破解每日签到
"""
import requests 
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

class WuaiQd(object):
    def __init__(self):
        # cookie
        self.cookie = ''
        # wxpusher Token
        self.appToken = ''
        # wxpusher topicId
        self.topicId = ''

    def checkin(self):
        headers={
            'Cookie': self.cookie,
            'ContentType':'text/html;charset=gbk'
        }
        requests.session().get('https://www.52pojie.cn/home.php?mod=task&do=apply&id=2',headers=headers)
        a=requests.session().get('https://www.52pojie.cn/home.php?mod=task&do=draw&id=2',headers=headers)
        print(a.text)
        b=BeautifulSoup(a.text,'html.parser')
        c=b.find('div',id='messagetext').find('p').text

        msg = ""
        if "您需要先登录才能继续本操作"  in c: 
            msg = "Cookie失效"
        elif "恭喜"  in c:
            msg = "吾爱破解签到成功"
        else:
            msg = "吾爱破解签到失败"
        print(c)
        return msg

    # wxpusher推送
    def wxpusher_send(self, msg):
        url = "http://wxpusher.zjiecode.com/api/send/message"
        params = {"appToken": self.appToken, "topicId": self.topicId, "content": "吾爱破解签到：\n\n" + msg}
        response = requests.get(url=url, params=params).text
        print(response)

    def main(self):
        msg = self.checkin()
        self.wxpusher_send(msg)

# 云函数入口
def main_handler(event, context):
    run = WuaiQd()
    run.main()

if __name__ == '__main__':
    run = WuaiQd()
    run.main()
