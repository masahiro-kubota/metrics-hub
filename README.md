概要

HA が各デバイスの統合・認証・更新を肩代わり

HA から MQTT に状態配信 → Telegraf で購読

メリット

認証・多デバイス連携を HA に丸投げできて楽

設定が宣言的になり、追加デバイスの横展開が早い

MQTT は疎結合で拡張しやすい（他の処理もぶら下げやすい）

デメリット

HA＋MQTT＋Telegraf とコンポーネントが増える

MQTT のトピック設計（命名/単位/retained）にひと工夫必要

```
[SwitchBot/各デバイス/Health系連携] → [Home Assistant]
                                      → (MQTT pub)
                                     [MQTT Broker] → [Telegraf mqtt_consumer]
                                                     → [InfluxDB] → [Grafana]
```
