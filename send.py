import argparse

from send_dingtalk import SendDingTalk
from send_wechart import SendWeixin


def add(args):
     r = args.x + args
     print('x + y = ', r)

def sub(args):
     r = args.x - args
     print('x - y = ', r)

def send(args):
    if args.send_target == "dingding":
        SendDingTalk()
    if args.send_target == "weixin":
        SendWeixin()

parser = argparse.ArgumentParser(prog='')
subparsers = parser.add_subparsers(help='sub-command help')
#添加子命令 add
parser_a = subparsers.add_parser('pgy', help='add help')
parser_a.add_argument("-s", '--send', type=str, dest="send_target", help=u"sendTarget--> Ex:dingTalk,weixin")

#设置默认函数
parser_a.set_defaults(func=send)

args = parser.parse_args()
#执行函数功能
args.func(args)
