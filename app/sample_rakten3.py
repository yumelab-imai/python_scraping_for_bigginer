import csv
import requests
import sys
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed



# 外部ファイルからURLを読み込むanalysis_data/
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file]

print('urls')
print(urls)

product_divs = []
total_urls = len(urls)

##########################################
# STEP1: Collect items detail urls.
# Total 6575 urls
##########################################

def fetch_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.body
    product_divs = body.find_all('div', class_='dui-card searchresultitem')
    return product_divs

# ThreadPoolExecutorを使用して非同期にURLから情報を取得
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fetch_url, url): url for url in urls}
    for index, future in enumerate(as_completed(futures)):
        result = future.result()
        product_divs += result

        # 進行状態を表示
        progress_percentage = (index + 1) / total_urls * 100
        print(f"進行状態: {progress_percentage:.2f}% ({index + 1}/{total_urls})")

print('product_divs')
print(f"個数: {len(product_divs)}")
# print('一旦ここでストップ！！')
# sys.exit()




##############################################################################################################################
# STEP2: Collect specific urls concerned with regular expression 'https://www.rakuten.co.jp/〇〇/info.html'
# Total ??? urls
##############################################################################################################################


# 集合 (set):であって、リスト (list):ではないことに注意！ => ※注１
info_urls = set()  # 重複なくinfo_urlを保存するための集合


# 最初のループでscraping_urlを取得
scraping_urls = [div.find('h2').find('a').get('href') for div in product_divs if div.find('h2') and div.find('h2').find('a')]

print('スクレイピング_URL一覧')
for scraping_url in scraping_urls:
    print(scraping_url)
print(f"個数: {len(scraping_urls)}")

total_urls = len(scraping_urls)

# 商品詳細ページから特定のURLを非同期に取得する関数
def fetch_specific_url(scraping_url):
    product_response = requests.get(scraping_url)
    product_soup = BeautifulSoup(product_response.content, "html.parser")
    pagebody_div = product_soup.body.find('div', id='pagebody')
    
    if pagebody_div:
        info_link = pagebody_div.find('a', href=lambda x: x and "info.html" in x)
        if info_link:
            return info_link.get('href')
    return None


# ThreadPoolExecutorを使用して非同期に商品詳細ページから特定のURLを取得
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fetch_specific_url, scraping_url): scraping_url for scraping_url in scraping_urls}
    for index, future in enumerate(as_completed(futures)):
        specific_url = future.result()
        # specific_url: fetch_specific_url()関数が有効なURLを返した場合にTrueになります（Noneが返された場合はFalseになります）
        # specific_url not in info_urls: これは取得したspecific_urlがまだinfo_urlsという集合にないことを確認
        if specific_url and specific_url not in info_urls:
            info_urls.add(specific_url)
            print(f"specific_url: {specific_url}")

        # 進行状態を表示
        progress_percentage = (index + 1) / total_urls * 100
        print(f"進行状態: {progress_percentage:.2f}% ({index + 1}/{total_urls})")





##############################################################################################################################
# STEP3: Output urls list to CSV file
# Total ??? urls
##############################################################################################################################

with open('company_urls_20230819.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['会社情報_URL']) # ヘッダー行
    for info_url in info_urls:
        writer.writerow([info_url])





##############################################################################################################################
# STEP4: End of execution
# Development Tips
##############################################################################################################################

# ※注１
# リストと集合（set）の操作には微妙な違いがあります。

# リスト (list):

# リストに要素を追加するときはappend()メソッドを使用します。
# python
# Copy code
# my_list = []
# my_list.append("item")
# 集合 (set):

# 集合に要素を追加するときはadd()メソッドを使用します。集合は重複する要素を持たないため、add()メソッドを使用しても、すでにその要素が集合内に存在する場合は何も追加されません。
# python
# Copy code
# my_set = set()
# my_set.add("item")
# コードの中で、info_urlsは集合（set）として初期化されているので、要素を追加するためにはadd()メソッドを使用するのが正しいです。

# 一方、scraping_urlsはリストとして扱われているので、要素を追加するためにappend()メソッドを使用しています。

# このように、使用するデータ型によって要素の追加方法が異なります。