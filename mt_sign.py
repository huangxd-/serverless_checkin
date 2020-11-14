#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Time ： 2020/10/24 9:52
@Auth ： huangxd-
@Des : m-team签到脚本
@File ：mt_qd.py
@IDE ：PyCharm
@Motto：Another me.
m-team每日签到脚本
"""
import requests
import re
import traceback

requests.packages.urllib3.disable_warnings()

class MtQd(object):
    def __init__(self):
        # m-team你的个人id
        self.id=''
        # m-team确认地址
        self.verify_url = 'https://pt.m-team.cc/verify.php?returnto=%2F%2Fuserdetails.php%3Fid%3D%s' % self.id
        # m-team签到地址
        self.base_url = 'https://pt.m-team.cc/userdetails.php?id=%s' % self.id
        # wxpusher Token
        self.appToken = ''
        # wxpusher topicId
        self.topicId = ''
        # mt token
        self.token = ''

    def checkin(self):
    
        headers = {"Cookie": self.token}
        # 需要session保留cookie信息
        session = requests.Session()
        try:
            # 重定向之后的确认接口，需要调用一次
            session.get(url=self.verify_url, headers=headers).text
            msg = session.get(url=self.base_url, headers=headers).text
            moli = re.findall(r'([\d,]+\.\d+)', msg.split("魔力值")[1])[0]
            upload = re.findall(r'([\d,]+\.\d+ \w+)', msg.split("上傳量")[1])[0]
            download = re.findall(r'([\d,]+\.\d+ \w+)', msg.split("下載量")[1])[0]
            ratio = re.findall(r'([\d,]+\.\d+)', msg.split("分享率")[1])[0]
            now = re.findall(r'>(\d+)', msg.split("當前做種")[1])[0]
            last = re.findall(r'(\w+)<\/span', msg.split("最近動向")[1])[0]
            msg = "- 魔力值："+str(moli)+"\n- 上傳量："+str(upload)+"\n- 下載量："+str(download)+"\n- 分享率："+str(ratio)+"\n- 當前做種："+str(now)+"\n- 最近動向："+str(last)
            print(msg)
            return msg
        except:
            print(traceback.print_exc())
            msg = "cookie失效!!!"
            print(msg)
            return msg

    # wxpusher推送
    def wxpusher_send(self, msg):
        url = "http://wxpusher.zjiecode.com/api/send/message"
        params = {"appToken": self.appToken, "topicId": self.topicId, "content": "M-team签到：\n\n" + msg}
        response = requests.get(url=url, params=params).text
        print(response)

    def main(self):
        msg = self.checkin()
        self.wxpusher_send(msg)

# 云函数入口
def main_handler(event, context):
    run = MtQd()
    run.main()

if __name__ == '__main__':
    run = MtQd()
    run.main()
