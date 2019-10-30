# -*- coding:utf-8 -*-
# Author: Ivanlon 
# E-mail: ivanlon@foxmail.com

# TODO: the code is a big mess, form the code

import random
import re

from PIL import Image
from requests import get

from exmple.timed_send import TimedSendMsg
from utils import *


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

class TimedSendKayuyaOnPixiv(TimedSendMsg):
    def get_msg(self) -> dict:
        """
        :return:
        """
        def format_img(img_path):
            try:
                str = img_path.rsplit(".", 1)
                output_img_path = str[0] + ".jpg"
                im = Image.open(img_path)
                im.save(output_img_path)
                return output_img_path
            except:
                return None
        try:
            img_url = loop_once()
        except NameError:
            from kaguya_on_pixiv import loop_once
            img_url = loop_once()

        save_dir = QMSG_TMP_DIR
        file_name = img_url[img_url.rindex('/') + 1:]
        print(img_url)

        headers = self.kwargs.get('headers', None)
        proxies = self.kwargs.get('proxies', None)
        for i in range(3):
            try:
                print(f'{i} try...')
                print(img_url, headers, proxies, sep='\n')
                res = get(img_url, headers=headers, proxies=proxies)
            except Exception as e:
                print(e)
            else:
                print('succes, response headers: {}'.format(res.headers))
                break
        else:
            return {}

        img_path = os.path.join(save_dir, file_name)
        with open(img_path, 'wb') as pf:
            pf.write(res.content)

        img_path = format_img(img_path)
        if img_path is None:
            print('img is broken')
            return {}

        msg = QbotMessage()
        msg.add_text(file_name)
        msg.add_img(img_path)

        msg_dict = {}
        for tar in self.tar_qq:
            msg_dict[tar] = msg

        return msg_dict

def send_kaguya():
    qq = 'your qq ID'
    dir = r"your pic directory"
    timed_kaguya = TimedSendKaguya(qq, 5, tar=qq, dir=dir)
    timed_kaguya.run()

def send_kaguya_on_pixiv():
    qq = 'your qq ID'
    headers = {
        'Referer': 'https://app-api.pixiv.net/',
    }
    proxies = {
        'http': 'http://127.0.0.1:1080',
        'https': 'https://127.0.0.1:1080',
    }
    pix_kaguya = TimedSendKayuyaOnPixiv(tar_qq=qq, interval=30, headers=headers, proxies=proxies)
    pix_kaguya.run()

if __name__ == '__main__':
    send_kaguya_on_pixiv()
    # or
    # send_kaguya()