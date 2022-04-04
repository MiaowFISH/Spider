import logging
import os
from urllib.error import HTTPError
from urllib.request import urlretrieve

from fake_useragent import UserAgent
from PIL import Image
from requests_html import AsyncHTMLSession, HTMLSession

from merge import merge_pdf
from utilles import get_file_list


def get_response(url):
    headers = {
        "User-Agent": UserAgent().random,
        # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62",
    }
    session = HTMLSession()
    res = session.get(url=url, headers=headers)
    return res


def get_chapter_list(url):
    """获取每一本书的章节列表
    :param url: 书籍链接
    :return: 章节列表 [[url, title], [url, title], ...]
    """
    res = get_response(url)
    if res.status_code != 200:
        logging.error("获取失败: %s" % url)
    temp = res.html.find(
        "body > div.container--response.de-container-wr.clearfix > div.de-container > div.de-chapter > div.chapter__list.clearfix > ul > li > a"
    )

    chapter_list = list(map(lambda x: [x.absolute_links, x.text], temp))
    return chapter_list


def get_pic_list(url):
    """获取每一章的图片列表
    :param url: 章节链接
    :return: 图片列表 [[url, alt], [url, alt], ...]
    """
    res = get_response(url)
    temp = res.html.find(
        "body > div.read-container > div.rd-article-wr.clearfix > div.rd-article__pic > img"
    )
    pic_list = list(
        map(lambda x: [x.attrs["dta-ec"], ("0" + x.attrs["alt"])[-6:]], temp)
    )
    # 怎么map出来是set啊, 这个转换血压上来了
    return pic_list


# def download_pic(url, path):
#     """下载图片
#     :param url: 图片链接
#     :param alt: 图片名
#     """
#     if os.path.exists(path) and os.path.getsize(path) > 48:
#         print("已存在: %s" % path)
#         return
#     while True:
#         retry = 1
#         session = HTMLSession()
#         with closing(
#             session.get(url, headers={"User-Agent": UserAgent().random}, stream=True)
#         ) as res:
#             if res.status_code != 200:
#                 if retry >= 3:
#                     print("超过重试次数")
#                     break
#                 print("下载失败 {}, {}, 重试: {}/3".format(url, res.status_code, retry))
#                 retry += 1
#                 continue
#             chunk_size = 8  # 单次请求最大值
#             content_size = int(res.headers["content-length"])  # 内容体总大小
#             data_count = 0
#             with open(path, "wb") as file:
#                 for data in res.iter_content(chunk_size=chunk_size):
#                     file.write(data)
#                     data_count = data_count + len(data)
#                     now_jd = (data_count / content_size) * 100
#                     print(
#                         "\r 文件下载进度: %d%%(%d/%d) - %s"
#                         % (now_jd, data_count, content_size, path),
#                         end=" ",
#                     )
#             break

#         """
#         with open(path, "wb") as f:
#             f.write(res.content)
#             f.close()
#             print("下载完成: %s, 耗时: %s" % (path, time.time() - start_time))
#         """
def download_pic(url, path, name):
    """
    下载文件
    :param url: 文件链接
    :param path: 保存目录
    :param name: 文件名称
    :return: None
    """

    def reporthook(a, b, c):
        """
        显示下载进度
        :param a: 已经下载的数据块
        :param b: 数据块的大小
        :param c: 远程文件大小
        :return: None
        """
        print("\rDownloading: %5.1f%%" % (a * b * 100.0 / c), end="")

    filePath = os.path.join(path, name)
    if not os.path.isfile(filePath):
        logging.info("开始下载: %s" % url)
        logging.info("文件名: %s" % name)
        try:
            urlretrieve(url, filePath, reporthook=reporthook)
        except HTTPError:
            logging.error("网络错误! 下载失败: %s" % url)
        logging.info("下载完成: ")
    else:
        logging.info("Exist, Skip!")
    filesize = os.path.getsize(filePath)
    logging.info("文件大小: %.2f Mb" % (filesize / 1024 / 1024))


def cover_jpg_to_pdf(file):
    path, filename = file.rsplit("\\", 1)
    per_name, post_name = filename.rsplit(".", 1)
    img = Image.open(file)
    img.save(path + "\\" + per_name + ".pdf", "PDF", resolution=100.0, saveall=True)


if __name__ == "__main__":
    URL = "https://www.haoman6.com/comic/3860"
    chapter_list = get_chapter_list(URL)
    for chapter in chapter_list:

        chapter_url = list(chapter[0])[0]
        chapter_title = chapter[1]
        path = "H:\\SpiderDepositary\\pic\\" + chapter_title
        if not os.path.exists(path):
            os.makedirs(path)
        logging.info("正在获取图片列表: %s" % chapter_title)
        pic_info = get_pic_list(chapter_url)[0]
        logging.info("正在下载")
        for pic_info in get_pic_list(chapter_url):
            pic_url, pic_name = pic_info
            download_pic(pic_info[0], path, pic_info[1])

        file_list = get_file_list(path, ".jpg")
        for i in file_list:
            cover_jpg_to_pdf(i)
        pdf_path = "H:\\SpiderDepositary\\pic"
        msg = merge_pdf(path, pdf_path + "\\" + chapter_title + ".pdf")
        logging.info(msg)
