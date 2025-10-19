# metrics-hub

Home Assistant + MQTT + Telegraf + InfluxDB + Grafana を使った統合監視システム

## 概要

- **Home Assistant**: デバイスの統合・認証・更新を担当
- **MQTT (Mosquitto)**: HAから状態をパブリッシュ
- **Telegraf**: MQTTメッセージを購読してInfluxDBに送信
- **InfluxDB**: 時系列データの保存
- **Grafana**: データの可視化・ダッシュボード

## クイックスタート

```bash
git clone <このリポジトリ>
cd metrics-hub
./setup.sh
```

## アクセス情報

- **Grafana**: http://localhost:3000 (admin/admin)
- **InfluxDB**: http://localhost:8086
- **Home Assistant**: http://localhost:8123

## MQTTテスト

```bash
# メッセージ送信テスト
docker exec mosquitto mosquitto_pub -h localhost -u hauser -P hapass -t 'ha/sensors/test/state' -m '{"temperature":22.5,"humidity":65}'
```

## メリット

- 認証・多デバイス連携をHAに丸投げできて楽
- 設定が宣言的になり、追加デバイスの横展開が早い  
- MQTTは疎結合で拡張しやすい

## デメリット

- コンポーネントが増える
- MQTTのトピック設計（命名/単位/retained）にひと工夫必要

```
[SwitchBot/各デバイス/Health系連携] → [Home Assistant]
                                      → (MQTT pub)
                                     [MQTT Broker] → [Telegraf mqtt_consumer]
                                                     → [InfluxDB] → [Grafana]
```
