from requests_html import HTMLSession

session = HTMLSession()
url = "https://igg-games.com/?s=minecraft&__cf_chl_f_tk=IlBd_Wylmz03QQS9aKfPkF2XpgD0FKGiz4Qj3Ev7ji4-1642226256-0-gaNycGzNB2U"
h = session.get(url=url)
print(h.html.find("div", first=True))
# print(h.html.html)
