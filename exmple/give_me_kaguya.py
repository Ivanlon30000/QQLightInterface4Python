# -*- coding:utf-8 -*-
# Author: Ivanlon 
# E-mail: ivanlon@foxmail.com

import random

from exmple.timed_send import TimedSendMsg
from util import *

class TimedSendKaguya(TimedSendMsg):
    def get_msg(self) -> dict:
        """
        每次发送辉夜大小姐的图片
        :return:
        """
        IMG_DIR = self.kwargs['dir']
        TAR = self.kwargs['tar']

        while True:
            file = random.choice(os.listdir(IMG_DIR))
            path = os.path.join(IMG_DIR, file)

            if os.path.isfile(path):
                msg = QbotMessage()
                msg.add_text(file)
                msg.add_img(path)
                msg = msg.boil()
                msg = {
                    TAR: msg
                }
                return  msg

if __name__ == '__main__':
    qq = '1049107917'
    dir = r'D:\Pictures\Kaguya-sama'
    timed_kaguya = TimedSendKaguya(qq, 60, tar=qq, dir=dir)
    timed_kaguya.run()