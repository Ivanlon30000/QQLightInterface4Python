# -*- coding:utf-8 -*-
# Author: Ivanlon 
# E-mail: ivanlon@foxmail.com

from time import sleep

from util import *

class TimedSendMsg():
    """定时发送消息"""

    def __init__(self, tar_qq:str or list, interval, **kwargs):
        """
        :param tar_qq: 目标QQ
        :param interval: 间隔
        """
        if isinstance(tar_qq, str):
            self.tar_qq = [tar_qq]
        self.interval = interval
        self.kwargs = kwargs

    def get_msg(self) -> dict:
        """
        :return:
        """
        raise FuncUndefinedError()

    def send_msg(self, msg_pairs):
        """

        :return:
        """
        for qq in self.tar_qq:
            msg = msg_pairs.get(qq, None)
            if msg is not None:
                send_message(qq, 'private', msg)
            else:
                msg = msg_pairs.get('*', None)
                if msg is not None:
                    send_message(qq, 'private', msg)

    def loop(self):
        """
        循环控制
        :return:
        """
        while True:
            content = self.get_msg()
            self.send_msg(content)
            sleep(self.interval)

    def run(self):
        """
        启动
        :return:
        """
        self.loop()