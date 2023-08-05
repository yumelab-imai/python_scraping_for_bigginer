print("Hello World!!!")

from bs4 import BeautifulSoup

# HTMLの一部を文字列として指定します。
html = """
<div data-asin="" data-index="69">
"""

# BeautifulSoupのオブジェクトを作成します。
soup = BeautifulSoup(html, 'html.parser')

# <div>タグを見つけ、'data-index'の値を取得します。
div = soup.find('div')
data_index = div.get('data-index')

print(data_index)  # このコードは "69" を出力します。