# -*- coding:utf-8 -*-
# Author: Ivanlon 
# E-mail: ivanlon@foxmail.com

import os
from pickle import load, dump

from requests import get
from bs4 import BeautifulSoup

from util import NetworkError, msgout
from exmple.timed_send import TimedSendMsg


class WhereIsMyNotice:
    def __init__(self, main_url=r'http://eis.whu.edu.cn/index.shtml',
                 interval=3600,
                 data_path=os.path.join('.', 'eis_notice_data', 'data.pkl'),
                 parser=None
                 ):
        self.main_url = main_url
        self.interval = interval
        self.data_path = data_path
        dir, file_name = os.path.split(data_path)
        if not os.path.exists(dir):
            os.makedirs(dir)

        if parser is None:
            self.parser = {
            '学院新闻': lambda soup: soup.find('div', class_='cont_nav lunbo-news'),
            '学院通知': lambda soup: soup.find_all('div', class_='cont_nav')[1],
            '学术动态': lambda soup: soup.find_all('div', class_='cont_nav')[2],
            '信息公开': lambda soup: soup.find('div', class_='cont_nav cont_right'),
            }
        else:
            self.parser = parser

    def com_url(self, url):
        if url.startswith('http'):
            return url
        else:
            return self.main_url[:self.main_url.rindex('/') + 1] + url

    def get_html(self):
        res = get(self.main_url)
        text = res.text
        if res.status_code != 200 or text == '':
            raise NetworkError()

        soup = BeautifulSoup(text, 'lxml')
        return soup

    def parse_html(self, soup) -> dict:
        data = {}
        for cat, method in self.parser.items():
            data[cat] = {}
            node = method(soup)
            cat = cat
            for tag in node.ul.find_all('li'):
                title = tag.a.text.strip()
                url = self.com_url(tag.a['href'])
                data[cat][title] = url
        return data

    def load_data(self):
        with open(self.data_path, 'rb') as f:
            id_data = load(f)
        return id_data

    def get_id(self, url):
        return url[url.rindex('/')+1:]

    def save_data(self, data):
        old_data = []
        for cat, news_dict in data.items():
            for title, url in news_dict.items():
                old_data.append(self.get_id(url))

        with open(self.data_path, 'wb') as f:
            dump(old_data, f)

    def compare(self, data: dict):
        old_data = self.load_data()

        new_data = {}
        del_cat = []
        for cat, news_dict in data.items():
            new_data[cat] = {}
            for title, url in news_dict.items():
                if self.get_id(url) not in old_data:
                    new_data[cat][title] = url

            if len(new_data[cat]) == 0:
                del_cat.append(cat)

        for each in del_cat:
            data.__delitem__(each)

        return data

    def clear(self):
        msgout('开始清理...')
        try:
            if os.path.exists(self.data_path):
                dir, file_name = os.path.split(self.data_path)
                os.remove(dir)
        except PermissionError as e:
            msgout('清理失败: {}'.format(e), 3)
        else:
            msgout('清理完成')

    def check(self) -> dict:
        msgout('检查学院官网...')
        try:
            soup = self.get_html()
        except NetworkError as e:
            msgout('网络错误 {}'.format(e), 2)
            raise NetworkError(e)
        else:
            data = self.parse_html(soup)
            self.save_data(data)
            new_news = self.compare(data)
            if len(new_news):
                msgout('有新的通知')
            else:
                msgout('没有新的通知')
            return new_news

class TimedEISNotice(TimedSendMsg):
    def __init__(self, tar_qq: str or list, interval, eis_cls:WhereIsMyNotice, **kwargs):
        self.eis_cls = eis_cls
        super().__init__(tar_qq, interval, **kwargs)

    def get_msg(self) -> dict:
        eis = self.eis_cls
        data = eis.check()

        data_list = []
        for cat, news_dict in data.items():
            data_list.append(cat+':')
            for title, url in news_dict.items():
                data_list.append('《{}》[{}]'.format(title, url))

        data_dict = {
            '*': data_list
        }

        print('data:',data_dict)

        return data_dict