from pprint import pprint
import requests
import zipfile
import json
from typing import Any, Dict, List
from io import BytesIO
URL_DETAIL = "https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web"
URL_IMAGE_INDEX = "https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web"
URL_MANGA_HOST = "https://manga.hdslb.com"
URL_IMAGE_TOKEN = "https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web"


def download(url: str, filename: str):
    with requests.get(url, stream=True) as r, open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def getChapters(comic_id: int) -> List[Any]:
    data = requests.post(
        URL_DETAIL, json={"comic_id": comic_id}).json()["data"]
    print("[Info]", data["title"])
    print("[Info]", data["evaluate"])
    data["ep_list"].reverse()
    return data["ep_list"]


def decode(data: bytearray, comic_id: int, ep_id: int) -> Dict[str, Any]:
    key = [
        ep_id & 0xff, ep_id >> 8 & 0xff, ep_id >> 16 & 0xff, ep_id >> 24 & 0xff,
        comic_id & 0xff, comic_id >> 8 & 0xff, comic_id >> 16 & 0xff, comic_id >> 24 & 0xff]
    for i in range(len(data)):
        data[i] ^= key[i % 8]
    with BytesIO(data) as f, zipfile.ZipFile(f) as z:
        data = json.loads(z.read("index.dat"))
    return data


def getImageIndex(comic_id: int, ep_id: int) -> Dict[str, Any]:
    data = requests.post(URL_IMAGE_INDEX, json={"ep_id": ep_id}).json()["data"]
    data = bytearray(requests.get(data["host"]+data["path"]).content[9:])
    return decode(data, comic_id, ep_id)


def getFullUrls(urls: List[str]) -> List[str]:
    data = requests.post(
        URL_IMAGE_TOKEN, json={"urls": json.dumps(urls)}).json()["data"]
    return [e["url"]+"?token="+e["token"] for e in data]


def main():
    # pprint(getChapters(29665))
    pprint(getFullUrls(getImageIndex(28566, 666687)["pics"]))


if __name__ == "__main__":
    main()
