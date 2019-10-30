# -*- coding:utf-8 -*-
# Author: Ivanlon 
# E-mail: ivanlon@foxmail.com

# TODO: the code is a big mess, form the code

from pixivpy3 import *

PROXY = {
    'http': "http://127.0.0.1:1080",
    'https': "https://127.0.0.1:1080"
}
HEADERS = {
    'Referer': 'https://app-api.pixiv.net/'
}
from http.client import RemoteDisconnected
from urllib3.exceptions import ProxyError
from pixivpy3.utils import PixivError

TOKEN_LOGIN = 1
access_token = 'your access token'
refresh_token = 'your refresh token'
user_id = 'your pixiv user id'
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
            l.append(name)
            l.append(': ')
            l.append(str(values[index]))
            l.append('\n')
        return ''.join(l)

def auth():
    """
    认证
    :return:
    """
    api = AppPixivAPI(proxies=PROXY)
    api.set_accept_language('zh-cn')
    if TOKEN_LOGIN:
        api.set_auth(access_token=access_token, refresh_token=refresh_token)
    else:
        api.login('your pixiv name', 'your pixiv password')
    print(api.access_token)
    print(api.refresh_token)
    return api

api = auth()
id = user_id
print(id)
detail = api.user_detail(id)
bookmarks = api.user_bookmarks_illust(id)
print(bookmarks)
my_marks = [work['id'] for work in bookmarks['illusts']]
print(detail)
print(bookmarks)

def loop_once():
    def get_all_favor_works(max_retries=3):
        """
        获取所有已收藏的插画
        :return:
        """
        for i in range(max_retries):
            print(f'{i} try...')
            favor_works = []
            try:
                bookmarks = api.user_bookmarks_illust(id)
                while True:
                    favor_works.extend([ImgOpt(illust) for illust in bookmarks.illusts])
                    if bookmarks.next_url is None:
                        print('success')
                        return favor_works
                    print('next_url', bookmarks.next_url)
                    next_qs = api.parse_qs(bookmarks.next_url)
                    print('next_qs', next_qs)
                    bookmarks = api.user_bookmarks_illust(**next_qs)

            except (PixivError, ProxyError, RemoteDisconnected) as e:
                print(f'error: {e}')
                pass

        print(f'{max_retries} failed, return None')
        return None

    favor_workers = get_all_favor_works()
    from random import choice, choices

    worker = choice(favor_workers)
    print(favor_workers)
    print(worker)

    def is_good_enough(work) -> bool:
        """
        插画足够棒
        :param work:
        :return:
        """
        if not isinstance(work, ImgOpt):
            work = ImgOpt(work)

        if 'R-18' in work.tags or \
                '四宮かぐや' not in work.tags or \
                work.id in my_marks or \
                '藤原千花' in work.tags:
            return False

        mark_percent = work.marks / work.views
        if (work.marks > 5000 and mark_percent > 0.6) or \
                (mark_percent > 0.1 and work.views > 100):
            return True

        return False

    def random_get_related(works, max_retries=3):
        for i in range(max_retries):
            try:
                print(f'{i} try get random related')
                ran_get = lambda x: choices(x, k=int(len(x) / 5) or 1)
                illust_ids = [work.id for work in ran_get(works)]
                several_illusts = []
                for illust_id in illust_ids:
                    several_illusts += api.illust_related(illust_id).illusts
                selected = [work for work in several_illusts if is_good_enough(work)]
                if selected:
                    print('get one good enough')
                    return choice(selected)
            except (PixivError, ProxyError, RemoteDisconnected) as e:
                print(f'error: {e}')
                pass
        print('fail')
        return None

    determined_illust = random_get_related(favor_workers)

    return determined_illust['image_urls']['large']

