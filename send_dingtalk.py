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
    _size = float(sizeStr) / 1024 / 1024
    version = '版本：{} (build {})'.format(jsonContent['buildVersion'], jsonContent['buildBuildVersion'])
    size = "大小：{:.2f} MB".format(_size)
    update_time = "更新时间 ：{}".format(jsonContent['buildUpdated'])
    open_url_path = 'https://www.pgyer.com/' + jsonContent['buildShortcutUrl']
    download_url_path = open_url_path
    picUrl = jsonContent['buildQRCodeURL']
    title = "请点击我测试\n{0}".format(jsonContent["buildName"])

    updateDes = input("此次更新内容：\n")
    _updateDes = "此次更新内容：" + updateDes
    _news = {
        "msgtype": "markdown",
        "markdown": {
            "title": "测试包下载",
            "text": "# {0} \n ### {1} \n ### {2} \n ### {3} \n ### {4} \n > ![screenshot]({5}) \n\n > [直接下载]({6}) \n".format(
                jsonContent["buildName"],
                version,
                size,
                update_time,
                _updateDes,
                picUrl,
                download_url_path)
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
            # print(current_app_detail)
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

    # hook = "https://oapi.dingtalk.com/robot/send?access_token=b0d71fd971f6399c3959fb12fe38a185c295d18eeb90b4c990bdf75c5af2124d"
    # current_app_detail = Pgy().get_current_app_detail()
    # print(current_app_detail)
    # sendToDingTalk(hook, current_app_detail)
