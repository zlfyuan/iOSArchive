#!/usr/bin/env python
# coding=utf-8

import unidecode
import json
import os
import requests
from config import ARCConfig, TargetSection
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
    picUrl = jsonContent['iconUrl']
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
    print(download_url_path)
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
        print('发送成功')
        return True
    else:
        print(rp['errmsg'])
        return False


class SendDingTalk:

    def __init__(self):
        try:
            hook = ARCConfig.getConfig(TargetSection, "dingTalk_hook")
            current_app_detail = Pgy().get_current_app_detail()
            sendToDingTalk(hook, current_app_detail)
        except:
            print("❌无法获取到机器人地址！！！")
            hook = input("请重新输入:")
            current_app_detail = Pgy().get_current_app_detail()
            if sendToDingTalk(hook, current_app_detail) == True:
                ARCConfig.saveConfig(TargetSection, "dingTalk_hook", hook)
            pass


if __name__ == '__main__':
    SendDingTalk()
