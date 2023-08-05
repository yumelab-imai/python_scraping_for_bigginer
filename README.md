## What it is?🧐
A repository for building Python development environments on your own PC using Docker.
This allows you to build an environment for scraping Python and LINE APIs, or for specific data on e-commerce sites, or to use AI tools such as Chat GPT at a more advanced level.

To set up a generic environment - using the Mac book Air's M2 chip.


## How to use it ?🧐

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


## ファイル一覧
| ファイル名 | 用途 |
| -------- | -------- |
| sample.py | Hello World 用 |
| sample_BeautifulSoup.py | foo |
| sample_url_request.py | foo |
| sample_output_csv | foo |
| sample_output_csv_about_puroducts.py | Amazon スクレイピング完了 |