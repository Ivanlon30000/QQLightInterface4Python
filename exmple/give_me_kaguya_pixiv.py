# -*- coding:utf-8 -*-
# Author: Ivanlon
# E-mail: ivanlon@foxmail.com

from http.client import RemoteDisconnected
from random import choice, choices

from PIL import Image
from pixivpy3 import *
from pixivpy3.utils import PixivError
from requests import get
from urllib3.exceptions import ProxyError

from exmple.timed_send import TimedSendMsg
from utils import *


class ImgOpt:
    """
    自定义的图片类
    """
    def __init__(self, img_data: dict):
        self.data = img_data
        self.id = img_data['id']
        self.title = img_data['title']
        self.img_url = img_data['image_urls']['large']
        self.caption = img_data['caption']
        self.user = img_data['user']
        self.tags = [tag_pair['name'] for tag_pair in img_data['tags']]
        self.trans_tags = [tag_pair['translated_name'] for tag_pair in img_data['tags']]
        self.views = img_data['total_view']
        self.marks = img_data['total_bookmarks']
        self.is_mark = img_data['is_bookmarked']

    def get_all(self):
        return (('id', 'title', 'img_url', 'caption', 'user', 'tags', 'trans_tags', 'views', 'marks', 'is_mark'),
                (self.id, self.title, self.img_url, self.caption, self.user, self.tags,
                 self.trans_tags, self.views, self.marks, self.is_mark))

    def __str__(self):
        names, values = self.get_all()
        l = []
        for index, name in enumerate(names):
            l.extend((name, ': ', str(values[index]), '\n'))
        return ''.join(l)

class KaguyaOnPixiv():
    """
    用于登录pixiv, 获取收藏记录, 获取图片链接
    """
    def __init__(self, username=None, password=None,
                 access_token=None, refresh_token=None, user_id=None,
                 proxies=None, **kwargs):
        """

        :param username:
        :param password:
        :param access_token:
        :param refresh_token:
        :param headers:
        :param proxies:
        :param kwargs:
        """
        api = AppPixivAPI(proxies=proxies)
        self.api = api

        self.max_retries = kwargs.get('max_retries', 3)

        if username is not None and password is not None:
            api.login(username, password)
            self.user_id = api.user_id
        elif access_token is not None and refresh_token is not None and user_id is not None:
            api.set_auth(access_token, refresh_token)
            self.user_id = user_id
        else:
            raise ValueError('You have to give a username-password pair '
                             'or an access token, refresh token and user ID pair to authorize')

    def refresh_bookmarks(self):
        """
        刷新收藏列表
        :return:
        """
        api = self.api

        for i in range(self.max_retries):
            msgout(f'Get bookmarks, {i + 1} trying...')
            bookmarks = []
            try:
                marks_page = api.user_bookmarks_illust(self.user_id)
                while True:
                    bookmarks.extend([ImgOpt(illust) for illust in marks_page.illusts])
                    if marks_page.next_url is None:
                        msgout('Get bookmarks successfully.')
                        msgout(f'bookmarks: {marks_page}', -1)
                        self.bookmarks = bookmarks
                        return bookmarks
                    msgout(f'next_url: {marks_page.next_url}', -1)
                    next_qs = api.parse_qs(marks_page.next_url)
                    msgout(f'next_qs: {next_qs}', -1)
                    marks_page = api.user_bookmarks_illust(**next_qs)

            except (PixivError, ProxyError, RemoteDisconnected) as e:
                msgout(f'{i + 1} try error: {e}')

        msgout(f'Get bookmarks {self.max_retries} tries failed, return old record', 2)
        return self.bookmarks

    def is_good_enough(self, work) -> bool:
        """
        插画足够棒
        :param work:
        :return:
        """
        api = self.api

        if not isinstance(work, ImgOpt):
            work = ImgOpt(work)

        if 'R-18' in work.tags or \
                '四宮かぐや' not in work.tags or \
                work.id in self.bookmarks or \
                '藤原千花' in work.tags:
            return False

        mark_percent = work.marks / work.views
        if (work.marks > 5000 and mark_percent > 0.6) or \
                (mark_percent > 0.1 and work.views > 100):
            return True

        return False

    def random_get_related(self, works, ran_get=None):
        """
        :param works:
        :param ran_get:
        :return:
        """
        api = self.api

        for i in range(self.max_retries):
            try:
                msgout(f'Randomly get similar illust, {i + 1} trying...')
                if ran_get is None:
                    ran_get = lambda x: choices(x, k=int(len(x) / 5) or 1)

                illust_ids = [work.id for work in ran_get(works)]
                several_illusts = []
                for illust_id in illust_ids:
                    several_illusts += api.illust_related(illust_id).illusts
                selected = [work for work in several_illusts if self.is_good_enough(work)]
                if selected:
                    msgout('Randomly get similar illust successfully.')
                    return choice(selected)

            except (PixivError, ProxyError, RemoteDisconnected) as e:
                msgout(f'{i + 1} try error: {e}', 2)

        msgout(f'Randomly get similar illust {self.max_retries} tries failed, return None', 2)
        return None

    def gen_url(self, title=False):
        """
        :return:
        """
        self.refresh_bookmarks()
        bookmarks = self.bookmarks
        if bookmarks is None:
            return None

        illust = self.random_get_related(bookmarks)
        if illust is None:
            return None
        try:
            url = illust['image_urls']['large']
        except KeyError as e:
            msgout(f'Extract url fail: {e}', 3)
            return None

        if title:
            try:
                title = illust['title']
            except KeyError as e:
                msgout(f'Extract caption fail: {e}', 3)
                return None

            return url, title
        else:
            return url

class TimedSendKayuyaOnPixiv(TimedSendMsg):
    """
    定时发送消息
    """
    def __init__(self, tar_qq: str or list, interval, **kwargs):
        pxnm = kwargs.get('pxnm', None)
        pxpw = kwargs.get('pxpw', None)
        pxat = kwargs.get('pxat', None)
        pxrt = kwargs.get('pxrt', None)
        pxid = kwargs.get('pxid', None)
        # pxpx = kwargs.get('pxpx', None)
        pxkw = kwargs.get('pxkw', {})

        self.save_dir = kwargs.get('save_dir', QMSG_TMP_DIR)
        self.headers = kwargs.get('headers', None)
        self.proxies = kwargs.get('proxies', None)
        self.max_retries = kwargs.get('max_retries', 3)

        pximg = KaguyaOnPixiv(username=pxnm, password=pxpw, access_token=pxat, refresh_token=pxrt, user_id=pxid,
                              proxies=self.proxies, **pxkw)
        self.pximg = pximg
        super().__init__(tar_qq, interval, **kwargs)

    @staticmethod
    def format_img(img_path):
        """
        从 pximg.net 下载下来的图片格式有问题, 需要转化一下
        :param img_path:
        :return:
        """
        try:
            str = img_path.rsplit(".", 1)
            output_img_path = str[0] + ".jpg"
            im = Image.open(img_path)
            im.save(output_img_path)
            return output_img_path
        except:
            return None

    def get_msg(self) -> dict:
        # Fundamental information
        res = self.pximg.gen_url(title=True)
        if res is not None:
            img_url, title = res
        else:
            msgout('Get img url failed, retry next loop', 3)
            return {}

        file_name = img_url[img_url.rindex('/') + 1:]
        msgout(f'img_url: {img_url}', -1)

        # Try to get http response
        for i in range(self.max_retries):
            try:
                msgout(f'Download img, {i+1} try...')
                res = get(img_url, headers=self.headers, proxies=self.proxies)
            except Exception as e:
                msgout(f'Failed {e}', 2)
            else:
                msgout(f'Download img successfully, illust title {title}')
                break
        else:
            msgout(f'{self.max_retries} tries failed, not to send msg', 3)
            return {}

        # Format the img file
        img_path = os.path.abspath(os.path.join(self.save_dir, file_name))
        with open(img_path, 'wb') as pf:
            pf.write(res.content)

        img_path = self.format_img(img_path)
        if img_path is None:
            msgout('Img is broken, not to send msg', 3)
            return {}

        # Construct msg
        msgout('Constructing msg...')
        msg = QbotMessage()
        msg.add_text(file_name)
        msg.add_img(img_path)

        msg_dict = {}
        for tar in self.tar_qq:
            msg_dict[tar] = msg

        msgout('Construct msg successfully')
        msgout(msg_dict, -1)

        return msg_dict

if __name__ == '__main__':
    # This 'headers' is important
    # DO NOT modify this 'headers' unless you definitely know
    # what you are doing
    headers = {
        'Referer': 'https://app-api.pixiv.net/',
    }

    # If you use proxy software, modify this
    proxies = {
        # 'http': 'http://127.0.0.1:1080',
        # 'https': 'https://127.0.0.1:1080',
    }

    qq = 'YOU_QQ_NUMBER'
    cool = 60*15
    px_username = 'YOUR_PIXIV_USERNAME'
    px_password = 'YOUR_PIXIV_PASSWORD'

    pix_kaguya = TimedSendKayuyaOnPixiv(
        tar_qq=qq,
        interval=cool,
        pxnm=px_username,
        pxpw=px_password,
        headers=headers,
        proxies=proxies
    )

    # If you want to authorize with token, use this:
    # px_access_token = 'YOUR_ACCESS_TOKEN'
    # px_refresh_token = 'YOUR_REFRESH_TOKEN'
    # px_user_id = 'YOUR_USER_ID'     # not username, important
    # pix_kaguya = TimedSendKayuyaOnPixiv(
    #     tar_qq=qq,
    #     interval=cool,
    #     pxat=px_access_token,
    #     pxrt=px_refresh_token,
    #     pxid=px_user_id,
    #     headers=headers,
    #     proxies=proxies
    # )
    pix_kaguya.run()