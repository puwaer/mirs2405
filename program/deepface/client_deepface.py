from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def handle_data():
    try:
        # クライアントからのデータを取得
        data = request.get_json()
        age = data.get('age')
        gender = data.get('gender')

        # 受信データの確認
        print(f"Received Data - Age: {age}, Gender: {gender}")

        # レスポンスを返す
        return jsonify({"status": "success", "message": "Data received successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # ホストIPとポートを設定
    app.run(host='172.25.15.27', port=5000)
