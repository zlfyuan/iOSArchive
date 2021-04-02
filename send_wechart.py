#!/usr/bin/env python
# coding=utf-8

import unidecode
import json
import os
import requests

from pgy import Pgy
from yamlPare import Yaml

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
                    "picurl": 'https://appicon.pgyer.com/image/view/app_icons/' + jsonContent['buildIcon']
                }
            ]
        }
    }
    print(download_url_path)
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
        print('转发到企业微信-->成功')
    else:
        print(rp['errmsg'])


class SendWeixin:

    def __init__(self):
        conf = Yaml().readValue()
        web_hook = conf["weChart"]["web_hook"]
        if web_hook == None and len(web_hook) == 0:
            web_hook = input("第一次请输入WebHook地址")
            current_app_detail = Pgy().getCurrentAppDetai()
            sendToWeixin(web_hook, current_app_detail)


if __name__ == '__main__':
    current_app_detail = Pgy().getCurrentAppDetai()
    sendWeixin(web_hook, current_app_detail)
