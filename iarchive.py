#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import argparse as apa

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

# xcodebuild -configuration Debug -target Lazy -xcconfig ./Lazy

def get_app_path(project):
    project_name = project
    derive_data = home_path + "/Library/Developer/Xcode/DerivedData"
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
                project_path = derive_data + "/" + "/Build/Products/Debug-iphoneos"
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

def projectName(name):
    app_path = get_app_path(name)
    update_des = input("请输入更新的日志描述:")
    ipa_path = bulidIPA(app_path) + "/Payload.ipa"
    pgy = Pgy()
    pgy.uploadIPA(ipa_path, update_des)


def sendToTester(sender):
    # print(sender)
    try:
        if sender == "weixin":
            SendWeixin()
        elif sender == "dingTalk":
            SendDingTalk()
        elif sender == "email":
            SendEmail()
        else:
            raise ValueError("缺少参数|参数错误，查看--help")
    except ValueError as e:
        print(e)


def showVersion(version):
    print("version:{0}".format(version))


if __name__ == '__main__':

    p = subprocess.Popen('xcodebuild -configuration Debug -workspace Lazy.xcworkspace  -scheme Lazy -xcconfig ./buildFile', shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    print("如果有错的话")
    print(err)
    for line in out.splitlines():
        print(line)

    # return
    # args = apa.ArgumentParser(prog="iarchive", description='iOS Application archive command tools', epilog='Information end ')
    #
    # args.add_argument("-a", '--archive', type=str, dest="name", default=None, help="your Project Target")
    #
    # args.add_argument("-s", '--send', type=str, dest="send_target", help=u"sendTarget--> Ex:dingTalk,weixin")
    #
    # args = args.parse_args()
    # print("argparse.args=", args, type(args))
    # # print("name = {0}".format(args.name))
    # d = args.__dict__
    # print(d)
    # if not "db" in d or d["db"] == None:
    #     # print("无效项目Target")
    #     pass
    # else:
    #     projectName(d["db"])
    #     # print("db",d["db"])
    #     # pass
    #
    # if d["send_target"] == None:
    #     # print("无效的发送目标")
    #     pass
    # else:
    #     sendToTester(d["send_target"])
    #     # print("send", d["send_target"])
    #     # pass
