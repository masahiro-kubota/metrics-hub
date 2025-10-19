FROM python:3.11-slim

# 必要なパッケージをインストール
RUN pip install --no-cache-dir psutil paho-mqtt

# 作業ディレクトリを設定
WORKDIR /app

# スクリプトをコピー
COPY memory_publisher.py .

# スクリプトに実行権限を付与
RUN chmod +x memory_publisher.py

# スクリプトを実行（バッファリング無効）
CMD ["python", "-u", "memory_publisher.py"]
