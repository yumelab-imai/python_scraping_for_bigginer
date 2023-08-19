import requests
from bs4 import BeautifulSoup
# 正規表現を扱うためのモジュール
import re
import csv
from datetime import datetime
# 複数のタスクを並行して実行する標準モジュール
from concurrent.futures import ThreadPoolExecutor, as_completed

# URLのリストを取得
with open('company_urls_20230819_complete.csv', 'r') as file:
    # ヘッダー行をスキップしてURLのリストを読み込む
    urls = [line.strip() for line in file.readlines()[1:]]

def fetch_company_info(url):
    try:
        # URLの内容を取得
        response = requests.get(url)
        response.raise_for_status()  # 無効な応答（4xx, 5xx）があった場合にエラーを生成
    except requests.RequestException as e:
        print(f"Error fetching URL {url}. Reason: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    company_info = soup.find('div', attrs={'id': 'companyInfo', 'class': 'c-spCompanyArea'})
    if not company_info:
        return None
    
    # 会社名
    name_tag = company_info.find('h1', class_='c-spCompanyName')
    name = name_tag.text.strip() if name_tag else "Not Applicable"

    # 電話番号
    phone_dds = company_info.find_all('dd')
    phone = "Not Applicable11"

    for dd in phone_dds:
        phone_match = re.search(r'TEL:([\d-]+)', dd.text)
        if phone_match:
            phone = phone_match.group(1)
            break

    # 会社住所
    address_dds = company_info.find_all('dd')
    address = "Not Applicable"

    for dd in address_dds:
        if re.search(r'〒', dd.text):
            address = dd.text.strip()
            break
    
    return name, address, phone, url

results = []

# ThreadPoolExecutorを使用して非同期に会社情報を取得
total_urls = len(urls)
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fetch_company_info, url): url for url in urls}
    for index, future in enumerate(as_completed(futures)):
        info = future.result()
        if info:
            results.append(info)

        # 進行状態を表示
        progress_percentage = (index + 1) / total_urls * 100
        print(f"進行状態: {progress_percentage:.2f}% ({index + 1}/{total_urls})")

# 現在の年月日と時刻を取得してファイル名に追加
now = datetime.now()
filename = f"specific_office_info_{now.strftime('%Y%m%d_%H%M')}.csv"

# CSVファイルに出力
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["会社名", "住所", "電話番号", "抽出元のURL"])  # ヘッダーを書き込む
    for row in results:
        writer.writerow(row)