from pprint import pprint
from requests_html import HTMLSession

session = HTMLSession()
url = "https://www.ykmh.com/manhua/monvzhilv/"
h = session.get(url=url)
ul = h.html.xpath("/html/body/div[3]/div[1]/div[2]/div[3]/ul")
pprint(list(map(lambda x: x.absolute_links, ul)))
