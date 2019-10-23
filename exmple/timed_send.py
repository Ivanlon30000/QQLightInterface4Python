# -*- coding:utf-8 -*-
# Author: Ivanlon 
# E-mail: ivanlon@foxmail.com

from time import sleep
from threading import Thread

from util import *

class TimedSendMsg():
    """定时发送消息"""

    def __init__(self, tar_qq:str or list, interval, max_cycles=0, **kwargs):
        """
        :param tar_qq: 目标QQ
        :param interval: 间隔
        """
        if isinstance(tar_qq, str):
            self.tar_qq = [tar_qq]
        self.interval = interval
        self.kwargs = kwargs
        self.cycles = 0
        self.max_cycles = max_cycles
        self.multi_cool = kwargs.get('multi_cool', 0.8)

    def get_msg(self) -> dict:
        """
        :return:
        """
        raise FuncUndefinedError()

    def __send_multi_msg(self, qq, multi_msg: list or tuple or set):
        """
        另起线程, 发送多消息
        :param qq:
        :param multi_msg:
        :return:
        """
        cooldown = self.multi_cool
        for msg_obj in multi_msg:
            send_message(qq, 'private', msg_obj)
            sleep(cooldown)

    def send_msg(self, msg_pairs):
        """
        :return:
        """
        for qq in self.tar_qq:
            msg = msg_pairs.get(qq, None)
            if msg is None:
                msg = msg_pairs.get('*', None)
                if msg is None:
                    continue

            if type(msg) in (list, tuple, set):
                # 多消息
                t = Thread(target=self.__send_multi_msg, args=(qq, msg))
                t.start()
            elif type(msg) in (str, QbotMessage):
                send_message(qq, 'private', msg)

    def loop(self):
        """
        循环控制
        :return:
        """
        while True:
            content = self.get_msg()
            self.send_msg(content)
            self.cycles += 1
            if self.cycles ==  self.max_cycles:
                print('**\t[INFO]达最大次数, 退出.')
                break
            sleep(self.interval)

    def run(self):
        """
        启动
        :return:
        """
        self.loop()