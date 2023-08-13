## ファイル一覧
| ファイル名 | 用途 |
| -------- | -------- |
| sample.py | Hello World 用 |
| sample_BeautifulSoup.py | foo |
| sample_url_request.py | foo |
| sample_output_csv | foo |
| sample_output_csv_about_puroducts.py | Amazon スクレイピング完了 |

## What it is?🧐



## How to use it ?🧐
<!-- 環境構築 -->
git clone https://github.com/yumelab-imai/python_development_environment_with_docker.git

cd python_development_environment_with_docker/
<!--  root  -->
```
<!-- イメージとコンテナの作成、コンテナの起動を実行 -->
docker compose up -d --build
<!-- コンテナが正常に起動したか確認 -->
docker container ls
// CONTAINER ID   IMAGE                 COMMAND                  CREATED          STATUS          PORTS                    NAMES
// 123445   jupyterlab-test-img   "jupyter-lab --ip 0.…"   13 seconds ago   Up 13 seconds   0.0.0.0:6666->6666/tcp   dev-jupyterlab
Python環境（コンテナ内）へ接続
docker compose exec -it jupyterlab bash
<!-- 動作確認(Heloo world を表示) -->
python3 sample.py
```

```
Jupyterlab の「token」確認
docker logs jupyterlab-test | tail
```


## 参考 URL
https://www.kagoya.jp/howto/cloud/container/dockerpython/


## ライブラリ補足
| モジュール | 用途 |
| -------- | -------- |
| pandas | CSV出力 |
| requests | 楽天市場の情報取得 |
| selenium | amazonの情報取得 |
| time | 処理の遅延（sleep） |
| selenium Select | ドロップダウンリストの操作 |
| BeautifulSoup | HTML解析（"味噌汁生成"） |


6725件の商品情報から
info.html部分を抽出!

150件のURLから6725件の商品情報を抽出! => 15分程度
6725件からinfo.html部分を抽出! => 2時間程度

<--- システムの概要 --->
・スクレイピングしたい楽天のURLを用意する。(今回の場合、楽天市場の商品一覧ページから、『韓国コスメ』で検索したときのURL) => 150件
=> URLから、商品データを取得する(今回の場合、6725件分の商品データ)
=> その中から楽天のWebページに設定されている会社情報があれば、それを重複がないように抽出する。
=> CSV 形式で出力する。
