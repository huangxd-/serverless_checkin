#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Time ： 2020/10/23 9:52
@Auth ： huangxd-
@Des : sspanel自动每日签到脚本
@File ：sspanel_qd.py
@IDE ：PyCharm
@Motto：Another me.
sspanel自动每日签到脚本，基于项目https://github.com/zhjc1124/ssr_autocheckin修改
"""
import requests
import re

requests.packages.urllib3.disable_warnings()

class SspanelQd(object):
    def __init__(self):
        # 机场地址
        self.base_url = 'https://xxx.xxx.xxx'
        # 登录信息
        self.email = ''
        self.password = ''
        # wxpusher Token
        self.appToken = ''
        # wxpusher topicId
        self.topicId = ''

    def checkin(self):
        email = self.email.split('@')
        email = email[0] + '%40' + email[1]
        password = self.password

        session = requests.session()

        session.get(self.base_url, verify=False)

        login_url = self.base_url + '/auth/login'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        post_data = 'email=' + email + '&passwd=' + password + '&code='
        post_data = post_data.encode()
        response = session.post(login_url, post_data, headers=headers, verify=False)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer': self.base_url + '/user'
        }

        response = session.post(self.base_url + '/user/checkin', headers=headers, verify=False)
        msg = (response.json()).get('msg')
        print(msg)

        info_url = self.base_url + '/user'
        response = session.get(info_url, verify=False)
        """
        以下只适配了CordCloud主题
        """
        try:
            used = re.findall(r'已用 \d+\.\d+% (\d+\.\d+\w+)', response.text)[0]
            rest = re.findall(r'剩余 \d+\.\d+% (\d+\.\d+\w+)', response.text)[0]
            expire = re.findall(r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})', response.text.split("等级过期时间")[1])[0]
            msg = "- 今日签到信息："+str(msg)+"\n- 已用流量："+str(used)+"\n- 剩余流量："+str(rest)+"\n- 到期时间："+str(expire)
            print(msg)
            return msg
        except:
            return msg

    # wxpusher推送
    def wxpusher_send(self, msg):
        if "续命过了" not in msg:
            url = "http://wxpusher.zjiecode.com/api/send/message"
            params = {"appToken": self.appToken, "topicId": self.topicId, "content": "CordCloud签到：\n\n" + msg}
            response = requests.get(url=url, params=params).text
            print(response)

    def main(self):
        msg = self.checkin()
        self.wxpusher_send(msg)

# 云函数入口
def main_handler(event, context):
    run = SspanelQd()
    run.main()

if __name__ == '__main__':
    run = SspanelQd()
    run.main()

