# -*- coding:utf-8 -*-
# Author: Ivanlon 
# E-mail: ivanlon@foxmail.com

import random
import re

from exmple.timed_send import TimedSendMsg
from util import *


class TimedSendKaguya(TimedSendMsg):
    def get_msg(self) -> dict:
        IMG_DIR = self.kwargs['dir']
        TAR = self.kwargs['tar']

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

                msg = {
                    TAR: msg
                }

                return  msg

if __name__ == '__main__':
    qq = '1049107917'
    dir = r"D:\Pictures\Kaguya-sama"
    timed_kaguya = TimedSendKaguya(qq, 5, tar=qq, dir=dir)
    timed_kaguya.run()