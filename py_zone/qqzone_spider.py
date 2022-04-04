#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""一个用于下载QQ空间相册内所有照片的爬虫"""

import logging
import os
import re
from json import loads

import filetype
import requests


class qqzone(object):
    """QQ空间相册爬虫"""

    def __init__(self, user):
        self.hostUin = user['hostUin']
        self.uin = user['uin']
        self.g_tk = user['g_tk']
        self.cookies = user['cookies']

    @staticmethod
    def get_path(album_name):

        path = 'D:/Miaow/Pictures/Saved Pictures/' + album_name
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def _login_and_get_args(self):
        """登录QQ，获取Cookies和g_tk"""

    def _init_session(self):
        self.session = requests.Session()

        self.session.headers = {
            'Referer': 'https://qzs.qq.com/qzone/photo/v7/page/photo.html?init=photo.v7/module/albumList/index&navBar=1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            'cookie': self.cookies
        }

    def _get_query_for_request(self, topicId=None, pageStart=0, pageNum=100):
        """获取请求相册信息或照片信息所需的参数

        Args:
            topicId: 每个相册对应的唯一标识符
            pageStart: 请求某个相册的照片列表信息所需的起始页码
            pageNum: 单次请求某个相册的照片数量

        Returns:
            一个组合好所有请求参数的字符串
        """
        query = {
            'g_tk': self.g_tk,
            'hostUin': self.hostUin,
            'uin': self.uin,
            'appid': 4,
            'inCharset': 'utf-8',
            'outCharset': 'utf-8',
            'source': 'qzone',
            'plat': 'qzone',
            'format': 'jsonp'
        }
        if topicId:
            query['topicId'] = topicId
            query['pageStart'] = pageStart
            query['pageNum'] = pageNum
        return '&'.join('{}={}'.format(key, val) for key, val in query.items())

    def _load_callback_data(self, resp):
        """以json格式解析返回的jsonp数据"""
        try:
            resp.encoding = 'utf-8'
            data = loads(re.search(r'.*?\(({.*}).*?\).*', resp.text, re.S)[1])
            return data
        except ValueError:
            logging.error('Invalid input')

    def _get_ablum_list(self):
        """获取相册的列表信息"""
        album_url = 'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?' + \
                    self._get_query_for_request()

        logging.info('Getting ablum list id...')
        resp = self.session.get(album_url)
        data = self._load_callback_data(resp)

        album_list = {}
        for item in data['data']['albumListModeClass']:
            if item['albumList'] is None:
                return album_list
            for albumList in item['albumList']:
                # for album in albumList:
                album_list[albumList['name']] = albumList['id']

        return album_list

    def _get_photo(self, album_name, album_id):
        """获取单个相册的照片列表信息，并下载该相册所有照片"""
        photo_list_url = 'https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_list_photo?' + \
                         self._get_query_for_request(topicId=album_id)

        logging.info('Getting photo list for album {}...'.format(album_name))
        resp = self.session.get(photo_list_url)
        data = self._load_callback_data(resp)
        if data['data']['totalInPage'] == 0:
            return None

        file_dir = self.get_path(album_name)
        for item in data['data']['photoList']:
            path = '{}/{}'.format(file_dir,
                                  item['uploadtime'].replace(':', ''))

            r = re.findall(r'(.+?)/', item['url'])
            url = '/'.join(('https://r.photo.store.qq.com',
                            r[2], r[3], r[4], 'r'))
            logging.info('Downloading {}-{} {}'.format(album_name,
                                                       item['uploadtime'], item['name']))
            self._download_image(url, path)

    def _download_image(self, url, path):
        """下载单张照片"""
        try:
            resp = self.session.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.content
                path = path + '.' + (filetype.guess(data).extension or 'jpg')
                if not os.path.exists(path):
                    open(path, 'wb').write(data)
                    logging.info('Done!')
                else:
                    logging.info('Skip!')
            else:
                logging.info(resp.status_code, url)
        except requests.exceptions.Timeout:
            logging.warning('get {} timeout'.format(url))
        except requests.exceptions.ConnectionError as e:
            logging.error(e.__str__)
        finally:
            pass

    def start(self):
        """爬虫的入口函数"""
        self._login_and_get_args()
        self._init_session()
        # album_list = self._get_ablum_list()
        album_list = {'唯美意境': 'V542WzQA4EP9Ir2AnPTH1FJwTk0b7Tnl'}
        for name, id in album_list.items():
            self._get_photo(name, id)


def main():
    FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    # 默认QQ账户信息
    user = {
        'hostUin': '25945856',
        'uin': '1293865264',
        'g_tk': '1238938739',
        'cookies': 'RK=amIh1bYadr; ptcz=c83ef8ee198a4096410eca86e76e871844ea7c2e8ba4ccc0d00c580574ac5705; qz_screen=1920x1080; QZ_FE_WEBP_SUPPORT=1; __Q_w_s__QZN_TodoMsgCnt=1; tvfe_boss_uuid=7e36b7c5b32509a1; pgv_pvid=6770509154; ptui_loginuin=704162514; __Q_w_s_hat_seed=1; sd_userid=12261621127004278; sd_cookie_crttime=1621127004278; cpu_performance_v8=12; o_cookie=1293865264; uin=o1293865264; skey=@vZVpT5Fje; p_uin=o1293865264; pt4_token=pYI1qKryNPZC-pqlXa6K*4MLN4k6*-TdpWSNTeFOeh0_; p_skey=wfmboGSlg7nh510ubHVR3k70UKP9pBGDPFK8tgkbP10_; Loading=Yes; pgv_info=ssid=s328872299; rv2=80C9656A1F1FE8B1B13572947810A8DDBEF0BF5567BD2EEF43; property20=46EC1FDE89860B5C560F4052FE0094D84CFCF356AA5B221AD248FAFCB97DE1FE0E8CB6C7F13E5BC6'
    }

    # 加 -d 参数可以使用上面的默认账户，默认信息请自行修改
    # if not (len(sys.argv) > 1 and sys.argv[1] == '-d'):
    #     user = get_user()

    qz = qqzone(user)
    qz.start()


if __name__ == '__main__':
    main()
