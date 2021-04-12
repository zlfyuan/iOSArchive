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
    _yaml = Yaml()
    object = _yaml.readValue()
    pgy = object
    weChart = {"web_hook": weburl}
    o = {"pgy": object, "weChart": weChart}
    _yaml.saveConfig(o)

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
                    "picurl": 'https://www.pgyer.com/image/view/app_icons/e067c6edb0ebcbf3fa55b17c31d2077e' +
                              jsonContent[
                                  'buildIcon'],
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
        try:
            _yaml = Yaml()
            object = _yaml.readValue()
            web_hook = object["weChart"]["web_hook"]
            current_app_detail = Pgy().get_current_app_detail()
            sendToWeixin(web_hook, current_app_detail)
        except ValueError as e:
            print("❌无法获取到企业微信机器人地址,请检查配置文件.dabao_config.yml 是否正确")


if __name__ == '__main__':
    SendWeixin()
