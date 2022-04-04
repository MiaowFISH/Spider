import requests


def save(file, data):
    with open(file, 'wb') as f:
        f.write(data)


# html = requests.get('https://manhua.dmzj.com/biedangounijiangle/')
# print(html.content)


for id in range(65537, 65540):
    for page in range(1, 14):
        url = 'http://i-cdn.ibuka.cn/pics/221735/{}/t5375921_{:0>4d}.jpg'.format(
            str(id), page)
        r = requests.get(url)
        print(url, r.status_code)
        if r.status_code == 200:

            save('D:\\Miaow\\Documents\\wwwroot\\buka\\img\\{}\\{:0>4d}.jpg'.format(
                id, page), r.content)
        else:
            print('下载失败')
            break
