#!/usr/bin/env python
# coding=utf-8

import unidecode
import json
import os
import requests

from pgy import Pgy
from yamlPare import Yaml
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
    picUrl = 'https://www.pgyer.com/image/view/app_icons/' + jsonContent[
                'buildIcon'],
    title = "请点击我测试\n 懒人易健"
    # 发送到钉钉群
    news = {
        "msgtype": "link",
        "link": {
            "text": description,
            "title": title,
            "picUrl": picUrl,
            "messageUrl": download_url_path
        }
    }
    _news = {
    "msgtype": "actionCard",
    "actionCard": {
        "title": jsonContent['buildName'],
        "text": "![screenshot]({0}) \n\n #### {1} \n\n {2}".format(picUrl,jsonContent['buildName'],description),
        "hideAvatar": "0",
        "btnOrientation": "0",
        "btns": [
            {
                "title": "点击进入测试",
                "actionURL": open_url_path
            }
        ]
    }
}
    # print(download_url_path)
    url = weburl
    data = _news
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
        _yaml = Yaml()
        object = _yaml.readValue()
        web_hook = object["dingTalk"]["web_hook"]
        current_app_detail = Pgy().get_current_app_detail()
        sendToDingTalk(web_hook, current_app_detail)


if __name__ == '__main__':
    SendDingTalk()
