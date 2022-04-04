import os
import re
from urllib.parse import unquote

import execjs
import js2xml
import requests
from lxml import etree


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Version/13.0.3 Mobile/15E148 Safari/604.1"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return etree.HTML(resp.text)
    else:
        exit(1)


def get_content(html):
    d = {}
    title = html.xpath('/html/body/div/div/div/div/div/span/a/h1')[0]
    li = html.xpath('/html/body/div/div/div[@class="middleright_mr"]/div/ul/li/a')
    for i in li:
        d[i.text] = i.attrib['href']
    return d


def get_script(html):
    """
    一定是漫画页
    """
    script = html.xpath('/html/head/script')[0].text
    return script


def get_chapter_name(html):
    config = js2xml.parse(get_script(html))
    return config.xpath('/program/var[@name=\'g_chapter_name\']/string/text()')[0]


def get_pic_path(html):
    script = 'function page(){' + get_script(html) + 'return arr_pages;}'
    return execjs.compile(script).call('page')


if __name__ == '__main__':
    path = 'D:\\Miaow\\Documents\\wwwroot\\buka\\img_1\\'
    # content_html = get_html('https://manhua.dmzj.com/biedangounijiangle/')
    # content = get_content(content_html)
    content = {'222': '/biedangounijiangle/79230.shtml'}
    for i, k in content.items():
        print(i, k)
        page_html = get_html('https://manhua.dmzj.com' + k)
        chapter_name = get_chapter_name(page_html)
        pic_path = get_pic_path(page_html)
        print(chapter_name, unquote(str(pic_path)))
        for i in pic_path:
            id = re.compile(r'\d+.jpg|\d+.png|\d+.JPG|\d+.PNG').findall(i)[0]
            if os.path.exists('{}{}_{}'.format(path, chapter_name, id)):
                print('{}_{} exists!'.format(chapter_name, id))
            else:
                r = requests.get('https://images.dmzj1.com/' + i)
                if r.status_code == 200:
                    file = '{}{}_{}'.format(path, chapter_name, id)
                    data = r.content
                    with open(file, 'wb') as f:
                        f.write(data)
                    print('Saved to {}{}_{}'.format(path, chapter_name, id))
