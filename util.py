# -*- coding:utf-8 -*-
# Author: Ivanlon 
# E-mail: ivanlon@foxmail.com
import json
import os
import time

import requests
import urllib3

from CONFIG import *

### Constant definition
MSGOUT_LEVEL = -2       # 忽略警告信息等级
__MSG_LEVEL = {
    -1: 'DEBUG',
    0: 'HINT',
    1: 'INFO',
    2: 'WARNING',
    3: 'ERROR'
}
HTTP_MANAGER = urllib3.PoolManager()


### Error definition
class FuncUndefinedError(Exception):
    pass

class NetworkError(Exception):
    pass


# Class definition
class QbotMessage():
    """
    构建一个统一的消息类
    """
    def __init__(self, tmp_dir='tmp'):
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        self.tmp_dir = tmp_dir
        self.content = []

    def __add_inner(self, content):
        """
        :return:
        """
        self.content.append(content)

    def add(self, ctype, content, **kwargs):
        """
        添加消息内容
        :param ctype: 消息类型
        :param content: 消息内容
        :param kwargs: 附加参数
        :return:
        """
        if ctype == 'text':
            # 文本消息
            self.__add_inner(content)
        elif ctype in ('img', 'pic'):
            # 是图片消息
            if content.startswith('http'):
                # 如果传入的是图片链接
                headers = kwargs.get('headers', None)
                proxies = kwargs.get('proxies', None)
                trans_src = kwargs.get('trans_src', True)
                if trans_src:       # 是否转储
                    res = requests.get(content, headers=headers, proxies=proxies)
                    if res.status_code == 200:
                        img_path = os.path.join(self.tmp_dir, 'pic_'+str(int(time.time())))
                        with open(img_path, 'wb') as pf:
                            pf.write(res.content)
                    else:
                        msgout('获取网络图片失败 {}'.format(res.status_code), 2)
                        return 'IMG URL ERROR'
                else:
                    img_path = content
            elif os.path.exists(content):
                # 如果传入的是本地图片地址
                img_path = content
            else:
                return 'IMG URL/PATH ERROR'
            self.__add_inner('[QQ:pic={}]'.format(img_path))
        else:
            pass

        return 'OK'

    def add_text(self, text, **kwargs):
        return self.add('text', text)

    def add_img(self, img, **kwargs):
        return self.add('img', img, **kwargs)

    def remove(self, index):
        """
        删除某个消息
        :param index:
        :return:
        """
        self.content.pop(index)

    def remove_last(self):
        """
        删除上一个消息
        :return:
        """
        self.remove(len(self.content)-1)

    def extend(self, msg_obj):
        """
        扩展
        :param msg_obj:
        :return:
        """
        self.content.extend(msg_obj)

    def boil(self):
        """
        转换成 QQ 格式的消息
        :return:
        """
        return ''.join(self.content)


### Function definition
def send_message_qqlight(tar_qq, msg_type, content_obj: str or QbotMessage, bot_ip=REMOTE_IP):
    """
    发送消息
    :param tar_qq:
    :param msg_type:
    :param content_obj:
    :param bot_ip: 机器人的ip地址
    :return:
    """
    # 1.好友消息 2.群消息 3.群临时消息 4.讨论组消息 5.讨论组临时消息 6.QQ临时消息
    pq = ''
    gq = ''
    if msg_type in (1, '1', '好友消息', 'private'):
        msg_type = 1
        pq = tar_qq
    elif msg_type in (2, '2', '群消息', 'group'):
        msg_type = 2
        gq = tar_qq
    elif msg_type in (3, '3', '群临时消息', 'temp_group'):
        msg_type = 3
        gq = tar_qq
    elif msg_type in (4, '4', '讨论组消息', 'discuss'):
        msg_type = 4
        gq = tar_qq
    elif msg_type in (5, '5', '讨论组临时消息', 'temp_discuss'):
        msg_type = 5
        gq = tar_qq
    elif msg_type in (6, '6', 'QQ临时消息', 'temp_private'):
        msg_type = 6
        pq = tar_qq
    else:
        raise ValueError('msg_type {} value error'.format(msg_type))

    # 内容
    if isinstance(content_obj, QbotMessage):
        content_obj = content_obj.boil()

    # request 参数
    url = 'http://{}:36524/api/v1/QQLight/Api_SendMsg'.format(bot_ip)
    data = {
        '类型': msg_type,
        '群组': gq,
        'qQ号': pq,
        '内容': content_obj
    }

    HTTP_MANAGER.request('POST', url,
                       body=json.dumps(data).encode('utf8'),
                       headers={"Content-Type": "application/json"}
    )

def send_message_test(tar_qq, msg_type, content_obj: str or QbotMessage, bot_ip=REMOTE_IP):
    print(tar_qq, msg_type, content_obj, bot_ip)

def msgout(msg, level=1, cmdline=True):
    """
    输出消息
    :param msg:
    :param level: 消息等级 0: hint, 1:info, 2:warning, 3:error
    :param cmdline:
    :return:
    """
    if level > MSGOUT_LEVEL:
        msg = '**\t[{}] {}'.format(__MSG_LEVEL[level].rjust(7), msg)
        if cmdline:
            print(msg)
        else:
            pass


### Abbreviation & Replacement
send_message = send_message_qqlight