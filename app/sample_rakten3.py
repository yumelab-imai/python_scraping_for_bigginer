import csv
import requests
from bs4 import BeautifulSoup

# 楽天のURL
# url = "https://www.rakuten.co.jp/category/562084/?l2-id=shop_header_rgenre3"


# 外部ファイルからURLを読み込むanalysis_data/
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file]

print('urls')
print(urls)

product_divs = []

# 各URLをループして情報を取得
for index, url in  enumerate(urls):
    # time.sleep(1)  # 1秒待つ
    # URLからWebページを取得
    response = requests.get(url)

    # BeautifulSoupオブジェクトを作成
    soup = BeautifulSoup(response.content, "html.parser")

    # <body>タグ内を取得
    body = soup.body

    # <body>タグ内の、dui-card searchresultitem クラスを含む div タグをすべて抽出
    product_divs += body.find_all('div', class_='dui-card searchresultitem')
    # 進行状態を表示
    progress_percentage = (index + 1) / len(urls) * 100 # 修正した箇所
    print(f"進行状態: {progress_percentage:.2f}% ({index + 1}/{len(urls)})") # こちらも修正

info_urls = set()  # 重複なくinfo_urlを保存するための集合
products = []

print('product_divs')
print(f"個数: {len(product_divs)}")


scraping_urls = []  # scraping_urlを保存するためのリスト

# 最初のループでscraping_urlを取得
for div in product_divs:
    scraping_url = div.find('h2').find('a')
    if scraping_url:
        scraping_urls.append(scraping_url.get('href'))

print('スクレイピング_URL一覧')
for scraping_url in scraping_urls:
    print(scraping_url)
print(f"個数: {len(scraping_urls)}")

info_urls = set()  # 重複なくinfo_urlを保存するための集合
total_urls = len(scraping_urls)

# scraping_urlを使って二回目のループでinfo_urlを取得
for index, scraping_url in enumerate(scraping_urls):
    # time.sleep(1)  # 1秒待つ
    # 商品URLから商品詳細ページを取得
    product_response = requests.get(scraping_url)
    product_soup = BeautifulSoup(product_response.content, "html.parser")

    # idがpagebodyであるdivタグを検索
    pagebody_div = product_soup.body.find('div', id='pagebody')

    if pagebody_div:
        # 商品詳細ページの中の https://www.rakuten.co.jp/〇〇/info.html を抽出
        info_link = pagebody_div.find('a', href=lambda x: x and "info.html" in x)
        if info_link:
            info_url = info_link.get('href')
            if info_url not in info_urls:  # 重複していない場合のみ処理を実行
                info_urls.add(info_url)  # 重複を防ぐため集合にURLを追加
                print(f"info_url: {info_url}")  # info_urlを表示

    # 進行状態を表示
    progress_percentage = (index + 1) / total_urls * 100
    print(f"進行状態: {progress_percentage:.2f}% ({index + 1}/{total_urls})")

print('会社情報_URL一覧')
for info_url in info_urls:
    print(info_url)


with open('company_urls_20230813.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['会社情報_URL']) # ヘッダー行
    for info_url in info_urls:
        writer.writerow([info_url])