dockerイメージをビルド
docker build -t deepface-app:latest .

コンテナを起動する
docker container run -it --name deepface-app -v $(pwd):/app deepface-app:latest


docker start -i deepface-app

python3 deepface_text.py

