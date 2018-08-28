## edgenode側
- sendData.pyを実行するとjson形式でデータ取得
  - BMX055.pyで9軸ジャイロデータ
  - GPSでみちびきのデータ取得
  - calibration.pyでジャイロと加速度センサで傾きをキャリブレーションしつつ求める
- host:宛先アドレス
- dt:何秒に1回データを送信するか
- port:ポート指定

### BMX055.pyの磁気センサのデータが取得できない問題
- BMC055.pyの50行目のコメントアウトを外して実行
- その後再び50行目をコメントアウトすると取得できる


## サーバ側
- udpserver.py実行で待機しておけばおk