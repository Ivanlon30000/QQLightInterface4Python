# -*- coding:utf-8 -*-
# Author: Ivanlon 
# E-mail: ivanlon@foxmail.com


import random
import re

from exmple.timed_send import TimedSendMsg
from utils import *


class TimedSendKaguya(TimedSendMsg):
    def get_msg(self) -> dict:
        IMG_DIR = self.kwargs['dir']

        while True:
            file = random.choice(os.listdir(IMG_DIR))
            title = re.search(r'title_([^_]*)_', file)
            title = title.group(1) if title is not None else os.path.splitext(file)[0]
            path = os.path.join(IMG_DIR, file)
            if os.path.isfile(path):
                msgout('发送 {}...'.format(file))
                msg = QbotMessage()
                msg.add_text(title)
                msg.add_img(path)
                msg_dict = {}
                for qq in self.tar_qq:
                    msg_dict[qq] = msg

                return msg_dict
            else:
                return {}


if __name__ == '__main__':
    qq = 'YOUR_QQ_NUMBER'
    dir = 'YOUR_PIC_DIRECTORY'
    cool = 60*15
    timed_kaguya = TimedSendKaguya(qq, interval=cool, dir=dir)
    timed_kaguya.run()