#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import subprocess

from pgy import Pgy
from send_wechart import SendWeixin
from send_dingtalk import SendDingTalk
from send_email import SendEmail
# 1。获得app路径
# 2。生成ipa包
# 3。登录蒲公英得到 key （保存key到文件）
# 4。上传ipa到蒲公英 （添加进度条）
# 5。通知测试用户
home_path = os.path.expandvars('$HOME')
conf_path = home_path + "/.dabao.yml"
# .daba_config.yml
def get_app_path():
    project_name = sys.argv[1]
    derive_data = home_path + "/Library/Developer/Xcode/DerivedData/"
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

if __name__ == '__main__':
    app_path = get_app_path()

    update_des = input("请输入更新的日志描述:")

    ipa_path = bulidIPA(app_path) + "/Payload.ipa"

    pgy = Pgy()

    pgy.uploadIPA(ipa_path, update_des)

    send_type = input("1.是否发送到企业微信?\n"
                      "2.是否发送到钉钉群?\n"
                      "3.是否发送到邮箱？\n\n"
                      "请选择对应类型的数字 Enter结束")
    if send_type == "1":
        sendWeixin()
    elif send_type == "2":
        sendDingTalk()
    elif send_type == "3":
        sendEmail()
    else:
        print("输入错误...")
        sys.exit()




