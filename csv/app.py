from flask import Flask, request, render_template, make_response
import pandas as pd
import requests
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_to_csv():
    try:
        # 외부 API에서 JSON 데이터 가져오기
        api_url = os.environ.get('API_URL')
        response = requests.get(api_url)
        json_data = response.json()

        # JSON 데이터를 DataFrame으로 변환
        df = pd.DataFrame(json_data)

        # CSV 파일로 변환
        csv_data = df.to_csv(index=False)

        # CSV 파일 다운로드
        response = make_response(csv_data)
        response.headers["Content-Disposition"] = "attachment; filename=data.csv"
        response.headers["Content-type"] = "text/csv"
        return response

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
