# presentationtimer
![sample](../../raw/images/window01.png)
## 使い方
### 起動方法
```
$ python3 presentationtimer.py  --help
usage: presentationtimer.py [-h] [-g 800x600] config

positional arguments:
  config                config file (ini format)

optional arguments:
  -h, --help            show this help message and exit
  -g 800x600, --geometry 800x600
                        window size
```
* 外部ライブラリには依存していません。標準ライブラリのみで動作します。
* `--geometory` オプションを指定しなければ、画面の最大サイズで起動します。
* 色などの設定は、表示内容と共に config ファイル内に記述します。
  * config ファイルは、このリポジトリ内の `sample.ini` をベースにして作成して下さい。

### 操作方法
* タイマーの開始
  * サンプル画面の「発表１のタイトル」部分をクリックします
* タイマーの停止
  * 発表時間と(あれば)質疑応答の時間がすぎれば、自動で停止します
  * 途中で止めたい場合は、サンプル画面の「発表１のタイトル」部分をクリックします
* タイマーのリセット
  * 現在の発表を最初からやり直す場合、サンプル画面の「発表１のタイトル」部分をダブルクリックします
* 次の発表に進める
  * サンプル画面の「発表２のタイトル」部分をクリックします
