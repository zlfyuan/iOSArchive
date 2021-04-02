#!/usr/bin/env python
# coding=utf-8

import unidecode
import json
import os
import requests

from pgy import Pgy

# 机器人地址
web_hook = ""

# 发送到钉钉
def sendToDingTalk(weburl, app_detail):
    jsonContent = app_detail
    sizeStr = jsonContent['buildFileSize']
    size = float(sizeStr) / 1024 / 1024
    description = '版本：{} (build {})  大小：{:.2f} MB 更新时间 ：{}'.format(jsonContent['buildVersion'],
                                                                   jsonContent['buildBuildVersion'],
                                                                   size,
                                                                   jsonContent['buildUpdated'])
    open_url_path = 'https://www.pgyer.com/' + jsonContent['buildShortcutUrl']
    download_url_path = open_url_path
    # 发送到钉钉群
    news = {
        "msgtype": "link",
        "link": {
            "text": description,
            "title": jsonContent['buildName'],
            "picUrl": 'https://appicon.pgyer.com/image/view/app_icons/' + jsonContent['buildIcon'],
            "messageUrl": download_url_path
        }
    }
    # print(download_url_path)
    url = weburl
    data = news
    h = {
        'Content-Type': 'application/json'
    }
    r = requests.post(url,
                      headers=h,
                      data=json.dumps(data)
                      )
    rp = json.loads(r.text)
    # print(rp)
    if rp['errcode'] == 0:
        print('\n转发到钉钉群-->成功...')
    else:
        print(rp['errmsg'])

class SendDingTalk:

    def __init__(self):
        web_hook = input("第一次请输入钉钉WebHook地址")
        if len(web_hook) != 0:
            current_app_detail = Pgy().getCurrentAppDetai()
            sendToDingTalk(web_hook, current_app_detail)

if __name__ == '__main__':
    current_app_detail = Pgy().getCurrentAppDetai()
    sendWeixin(web_hook, current_app_detail)
