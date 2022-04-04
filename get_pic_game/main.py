import asyncio

import aiohttp
from lxml import etree


async def get_html(id):
    async with aiohttp.ClientSession() as session:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) "
                          "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                          "Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        params = {'id': id}
        async with session.get('https://game.eroge.xyz/hhh.php', headers=headers, params=params) as resp:
            if resp.status == 200:
                return await resp.text()
            else:
                exit(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    id = 41
    html = loop.run_until_complete(get_html(id))
    html = etree.HTML(html)
    title = html.xpath('/html/body/h1')[0].text
    code = html.xpath('/html/body/h2')[0].text
    link = []

    html_list = html.xpath('/html/body/div/a[@class="layui-btn"]')
    for i in html_list:
        print(i.text, i.attrib['href'])
        link.append(i.attrib['href'])
    json_ = {
        'id': id,
        'title': title,
        'code': code,
        'link': link
    }
    print(json_)
