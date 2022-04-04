import js2xml
import requests
from bs4 import BeautifulSoup

headers = {
    'cookie': 't=d970fee880a8a21b3bc6c4cfc5214f06; cna=z9qXE/dcfB4CAXcx2lO5D6hy; miid=830238069184972498; UM_distinctid=163d4e10df42c9-008bee4f8dbd2e-6b1b1279-100200-163d4e10df531e; __guid=154677242.2026198364084961000.1528950691863.182; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; cookie2=1a9dd588fb9863dbcef85080ba49048d; v=0; _tb_token_=fb473336e3bee; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=1B0C308CF96CCA8721C294659D0603C2; monitor_count=8; CNZZDATA1272960300=1938859093-1528945321-https%253A%252F%252Fwww.taobao.com%252F%7C1528977724; isg=BGtrPwowtJC0BOh06VZZtSmH-o-VKH8KIAakd93oRqoBfIveZVAPUgne0rwS3Nf6',
    'referer': 'https://www.taobao.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
}

url = "https://manhua.dmzj.com/biedangounijiangle/92700.shtml"
r = requests.get(url, headers=headers)
demo = r.content
soup = BeautifulSoup(demo, 'lxml')
src = soup.select('head script')[0].string
src_text = js2xml.parse(src, encoding='utf-8', debug=False)
print(js2xml.pretty_print(src_text))
