Artnet-hid 変換サーバ
=====================
Artnet から HID に変換するサーバです。

Artnet のパケットには 128 個の RGB LED 分のデータが入っていることを想定しています。

-u オプションでユニバース番号を指定できます。
```
usage: artnet-hid.py [-h] [-u U]

artnet to hid

options:
  -h, --help  show this help message and exit
  -u U        universe to listen to
```

インストール方法
---------------
最近の python は、PEP 668 に基づき、ちゃんと venv やらで実行環境を分離せよということになっている。

以下インストール例。

### 最初に一回だけやるやつ
1. udev ルールを設定する
50-keyboard.rules に設定例がある。このままでも雑だけど取りあえず動く。
```
# cp 50-keyboard.rules /etc/udev/rules.d/
```

2. venv やらで環境つくって pip で必要なパッケージをインストールする
```sh
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```


### 実行時に毎回やるやつ
1. venv 有効化
```
$ source .venv/bin/activate
```

2. 実行
```
$ python artnet-hid.py
```