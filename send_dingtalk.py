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
            "picUrl": 'https://www.pgyer.com/image/view/app_icons/e067c6edb0ebcbf3fa55b17c31d2077e' + jsonContent[
                'buildIcon'],
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
        try:
            raise ValueError("❌无法获取到钉钉机器人地址,请检查配置文件.dabao_config.yml 是否正确")
            _yaml = Yaml()
            object = _yaml.readValue()
            web_hook = object["dingTalk"]["web_hook"]
            current_app_detail = Pgy().get_current_app_detail()
            sendToDingTalk(web_hook, current_app_detail)
        except ValueError as e:
            print(e)


if __name__ == '__main__':
    SendDingTalk()
