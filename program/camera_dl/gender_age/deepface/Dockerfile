# ベースイメージとしてPython 3.9を使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxrender1 libxext6 libopencv-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# OpenCVとDeepFaceのインストール
RUN pip install --no-cache-dir opencv-python-headless deepface
RUN pip install tf-keras
RUN pip install tensorflow==2.5.0
RUN pip install numpy>=1.22.4



# アプリケーションのコードをコンテナにコピー
COPY /. /app/

# メインスクリプトを実行
#CMD ["python", "your_script_name.py"]
CMD ["/bin/bash"]

