#!/bin/bash

# metrics-hub セットアップスクリプト
# git clone後に実行してください

set -e  # エラーが発生したら停止

echo "🚀 metrics-hub セットアップを開始します..."

# 1. Mosquitto パスワードファイルの生成
echo "📝 Mosquitto パスワードファイルを生成中..."
if [ ! -f "./mosquitto/config/passwd" ]; then
    docker run --rm \
        -v "$(pwd)/mosquitto/config:/config" \
        eclipse-mosquitto:2 \
        mosquitto_passwd -c -b /config/passwd hauser hapass
    echo "✅ パスワードファイルを生成しました"
else
    echo "ℹ️  パスワードファイルは既に存在します"
fi

# 2. InfluxDB 環境設定ファイルのコピー
echo "🗂️  InfluxDB 環境設定ファイルを準備中..."
if [ ! -f "./influxdb/env.list" ]; then
    if [ -f "./influxdb/example.env.list" ]; then
        cp "./influxdb/example.env.list" "./influxdb/env.list"
        echo "✅ env.list ファイルを作成しました"
    else
        echo "⚠️  example.env.list が見つかりません。空の env.list を作成します"
        touch "./influxdb/env.list"
    fi
elsedfdfdf
    echo "ℹ️  env.list ファイルは既に存在します"
fi

# 3. Docker Composeサービスの起動
echo "🐳 Docker Composeサービスを起動中..."
docker compose up -d

# 4. サービスの起動確認
echo "⏳ サービスの起動を待機中..."
sleep 10

# 5. 接続テスト
echo "🔍 サービス接続テスト..."
echo "  - InfluxDB (port 8086): http://localhost:8086"
echo "  - Grafana (port 3000): http://localhost:3000"
echo "  - Mosquitto (port 1883): tcp://localhost:1883"

# 6. Telegrafの接続状況確認
echo "📊 Telegrafの接続状況を確認..."
docker logs telegraf 2>&1 | tail -5 | grep -E "(Connected|Error)" || echo "  ログを確認してください: docker logs telegraf"

echo ""
echo "✅ セットアップ完了！"
echo ""
echo "📋 次のステップ:"
echo "  1. Grafana にアクセス: http://localhost:3000"
echo "     - ユーザー名: admin"
echo "     - パスワード: admin"
echo "  2. InfluxDB データソースを設定:"
echo "     - URL: http://influxdb:8086"
echo "     - Organization: myorg" 
echo "     - Token: mytoken"
echo "     - Bucket: mybucket"
echo "  3. MQTTメッセージをテスト:"
echo "     docker exec mosquitto mosquitto_pub -h localhost -u hauser -P hapass -t 'ha/sensors/test/state' -m '{\"temperature\":22.5,\"humidity\":65}'"
echo ""
