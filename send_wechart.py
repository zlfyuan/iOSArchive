#!/usr/bin/env python
# coding=utf-8

import unidecode
import json
import os
import requests

from pgy import Pgy
from config import ARCConfig, TargetSection

# 更新描述
updatades = '版本更新了'

# 机器人地址
web_hook = ""


# 发送到企业微信
def sendToWeixin(weburl, app_detail):
    jsonContent = app_detail
    sizeStr = jsonContent['buildFileSize']
    size = float(sizeStr) / 1024 / 1024
    description = '版本：{} (build {})  大小：{:.2f} MB 更新时间 ：{}'.format(jsonContent['buildVersion'],
                                                                   jsonContent['buildBuildVersion'],
                                                                   size,
                                                                   jsonContent['buildUpdated'])
    open_url_path = 'https://www.pgyer.com/' + jsonContent['buildShortcutUrl']
    download_url_path = open_url_path
    # 发送到企业微信群
    news = {
        "msgtype": "news",
        "news": {
            "articles": [
                {
                    "title": jsonContent['buildName'],
                    "description": description,
                    "url": download_url_path,
                    "picurl": jsonContent['iconUrl']
                }
            ]
        }
    }
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
        print(download_url_path)
        print('发送成功')
        return True
    else:
        print(rp['errmsg'])
        return False


class SendWeixin:

    def __init__(self):
        try:
            hook = ARCConfig.getConfig(TargetSection, "weChat_hook")
            current_app_detail = Pgy().get_current_app_detail()
            sendToWeixin(hook, current_app_detail)
        except:
            print("❌无法获取到机器人地址！！！")
            hook = input("请重新输入:")
            current_app_detail = Pgy().get_current_app_detail()
            if sendToWeixin(hook, current_app_detail) == True:
                ARCConfig.saveConfig(TargetSection, "weChat_hook", hook)

if __name__ == '__main__':
    SendWeixin()