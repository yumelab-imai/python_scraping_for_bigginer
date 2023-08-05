print("Hello World!!!")


import requests
from bs4 import BeautifulSoup


# AmazonのURL
url = "https://www.amazon.co.jp/s?k=%E9%9F%93%E5%9B%BD%E3%82%B3%E3%82%B9%E3%83%A1&__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=2HGHTZJ98Z987&sprefix=%E9%9F%93%E5%9B%BD%E3%82%B3%E3%82%B9%E3%83%A1%2Caps%2C194&ref=nb_sb_noss_1"

# URLからWebページを取得
response = requests.get(url)

# BeautifulSoupオブジェクトを作成
soup = BeautifulSoup(response.content, "html.parser")

# <body>タグ内を取得
body = soup.find('body')

# divタグでdata-index属性があるものをすべて抽出
div_tags = body.find_all('div', attrs={'data-index': True})


# 各divタグからdata-index属性の値を取得し、表示
for tag in div_tags:
    print(tag.get('data-index'))  # div タグの data-index 属性の "1" だったり、"69" などを出力


