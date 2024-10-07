# ベースイメージとしてPython 3.8を使用
FROM python:3.8-slim

# OpenCVや依存ライブラリをインストールするためのパッケージをアップデート
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    libglib2.0-0 \
    libgtk2.0-dev \
    pkg-config \
    curl \
    ca-certificates \
    && apt-get clean

# OpenCV, moviepy, argparse, Caffeモジュールなどの必要なPythonライブラリをインストール
RUN pip install --no-cache-dir \
    opencv-python-headless \
    moviepy \
    numpy \
    argparse

# Caffeモデルをダウンロードするスクリプトを用意
RUN mkdir -p /models && \
    curl -o /models/opencv_face_detector.pbtxt https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender/opencv_face_detector.pbtxt && \
    curl -o /models/opencv_face_detector_uint8.pb https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender/opencv_face_detector_uint8.pb && \
    curl -o /models/age_deploy.prototxt https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender/age_deploy.prototxt && \
    curl -o /models/age_net.caffemodel https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender/age_net.caffemodel && \
    curl -o /models/gender_deploy.prototxt https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender/gender_deploy.prototxt && \
    curl -o /models/gender_net.caffemodel https://raw.githubusercontent.com/spmallick/learnopencv/master/AgeGender/gender_net.caffemodel

# 作業ディレクトリを設定
WORKDIR /app

# 必要なPythonスクリプトをコンテナにコピー
COPY gender_deploy.py /gender_deploy.py

# モデルファイルをコンテナにコピー（Dockerfileにモデルファイルがあればこちらを使用）
COPY models/ /models/

# エントリーポイントのスクリプトを実行
ENTRYPOINT ["python", "/app/gender_deploy.py"]
