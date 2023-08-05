print("Hello World!!!")


import csv
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


# data-index属性値をリストに格納
data_index_values = [tag.get('data-index') for tag in div_tags]


# テスト完了
# print(data_index_values)  # div タグの data-index 属性の "1" だったり、"69" などを出力
# ['0', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53']


# CSVファイルへ書き込み
with open('analysis_data/data_index_values.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['data-index'])
    for value in data_index_values:
        writer.writerow([value])
