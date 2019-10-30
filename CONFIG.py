# -*- coding:utf-8 -*-
# Author: Ivanlon 
# E-mail: ivanlon@foxmail.com
import os

# QQ机器人所在IP
REMOTE_IP = 'localhost'

# QQ机器人的QQ号 (暂时没用)
BOT_ID = ''

# 发送消息间隔 (机器人发送消息过快会被腾讯拦截消息)
SEND_MESSAGE_INTERVAL = 0.8

# 忽略警告信息等级
MSGOUT_LEVEL = -2

# QBotMessage 类的临时文件夹
QMSG_TMP_DIR = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'tmp')