#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import os
import getpass
from bs4 import BeautifulSoup
import sys
import getopt
import subprocess

api_key_path = os.getcwd() + "/.this_is_apikey"


# 1。获得app路径
# 2。生成ipa包
# 3。登录蒲公英得到 key （保存key到文件）
# 4。上传ipa到蒲公英 （添加进度条）
# 5。通知测试用户

def get_app_path():
    project_name = sys.argv[1]
    derive_data = os.path.expandvars('$HOME') + "/Library/Developer/Xcode/DerivedData/"
    print(derive_data)
    if not os.path.exists(derive_data):
        print("找不到DerivedData文件 -->没有安装Xcode 或者 重启Xcode")
        sys.exit(1)
    with os.scandir(derive_data) as it:
        project_enable = False
        for entry in it:
            if project_name == entry.name.split("-")[0] and entry.is_dir():
                project_enable = True
                # print(entry.name)
                project_path = derive_data + "/" + entry.name + "/Build/Products/Debug-iphoneos"
                with os.scandir(project_path) as dir:
                    for file in dir:
                        if project_name + ".app" == file.name:
                            appfile_path = project_path + "/" + project_name + ".app"
                            print(appfile_path)
                            return appfile_path
        if not project_enable:
            print("找不到{0}文件 -->没有安装Xcode 或者 重启Xcode".format(project_name))
            sys.exit(1)


# 编译打包 得到ipa
def bulidIPA(app_path):
    dirs = app_path.split("/")
    dirs.pop()
    # print(dirs)
    app_dir = "/".join(dirs)
    pack_bag_path = app_dir + "/packBagPath"
    pay_load_path = app_dir + "/PayLoadPath"
    # print(packBagPath)
    # print(PayLoadPath)
    subprocess.call(["rm", "-rf", pack_bag_path])
    subprocess.call(["mkdir", "-p", pay_load_path])
    subprocess.call(["cp", "-r", app_path, pay_load_path])
    subprocess.call(["mkdir", "-p", pack_bag_path])
    subprocess.call(["cp", "-r", pay_load_path, pack_bag_path])
    subprocess.call(["rm", "-rf", pay_load_path])
    os.chdir(pack_bag_path)
    subprocess.call(["zip", "-r", "./Payload.zip", "."])
    print("\n打包成功...")
    subprocess.call(["mv", "payload.zip", "Payload.ipa"])
    subprocess.call(["rm", "-rf", "./Payload"])
    return pack_bag_path


# 获取apikey
def get_api_key():
    if os.path.exists(api_key_path):
        f = open(api_key_path, "r+")
        api_key = f.read()
        f.close()
        if len(api_key) != 32:
            print("\napi_key错误，重新登录")
            return pgy_api(login())[1]
        else:
            return api_key
    else:
        return pgy_api(login())[1]


# 登录蒲公英
def login():
    url = 'https://www.pgyer.com/user/login'
    email = input("请输入蒲公英账号 Enter结束：")
    password = getpass.getpass('请输入蒲公英密码 Enter结束：')
    data = {
        'email': email,
        'password': password
    }
    req = requests.post(url, data=data)
    req.encoding = 'UTF-8'

    rp = json.loads(req.text)
    # print(rp)
    status_code = rp['code']
    if status_code == 0:
        # print(req.cookies)
        return req.cookies
    else:
        print(rp['message'])
        login()


# 获取蒲公英api_key user_k
def pgy_api(cookies):
    user_url = 'https://www.pgyer.com/account/api'
    req_user = requests.get(url=user_url, cookies=cookies)
    req_user.encoding = 'UTF_8'
    b = BeautifulSoup(req_user.text, 'html.parser')
    code_tag = b.find_all("code")
    api_key = ''
    user_key = ''
    for i in range(len(code_tag)):
        n = code_tag[i]
        if i == 0:
            api_key = n.contents[0]
        else:
            user_key = n.contents[0]
    # print('api_key \t' + api_key)
    # print('user_key \t' + user_key)
    try:
        f = open(api_key_path, "w")
        f.write(api_key)
        f.close()
    except IOError:
        print("没有找到{0}".format(api_key_path))
    return user_key, api_key


def uploadIPA(ipa_path, updata_des):
    api_key = get_api_key()
    if (os.path.exists(ipa_path)):
        print("\n开始上传到蒲公英...")
        url = 'https://www.pgyer.com/apiv2/app/upload'
        data = {
            '_api_key': api_key,
            'buildInstallType': '3',
            'buildPassword': '',
            'buildUpdateDescription': updata_des
        }
        loading = True
        st = 'send.'
        # while loading:
        #     st += "."
        #     print(st)
        files = {'file': open(ipa_path, 'rb')}
        r = requests.post(url, data=data, files=files)
        r.encoding = 'UTF-8'
        r = json.loads(r.text)
        status_code = r['code']
        if status_code == 0:
            # loading = False
            print("上传成功...")
        else:
            # loading = False
            raise Exception("\n%s - %s..." % (r['message'], r['code']))
    else:
        raise Exception("\n没有找到iap包...")


if __name__ == '__main__':

    app_path = get_app_path()

    update_des = input("请输入更新的日志描述:")

    ipa_path = bulidIPA(app_path) + "/Payload.ipa"

    uploadIPA(ipa_path, update_des)
