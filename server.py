# 서빙 할 모델 경로
MODEL_PATH = "runs/classify/train/weights/best.pt"


###############################################################
from flask import Flask, request, jsonify
from ultralytics import YOLO
import os
from PIL import Image
import numpy as np

# Flask 앱 생성
app = Flask(__name__)

# YOLO 모델 로드
print("Loading YOLO model...")
model = YOLO(MODEL_PATH)

# warm-up
print("Warming up the YOLO model...")
[model(np.zeros((160, 160, 3), dtype=np.uint8), verbose=False) for _ in range(3)] 


print("Server is ready to accept requests.")
@app.route('/', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    try:
        # 이미지를 저장하지 않고 PIL로 바로 열기
        image = Image.open(file.stream)

        # YOLO 모델로 예측 수행
        result = model.predict(
            source = image, 
            verbose=True
        )[0]

        ### 공통 데이터 정보 (result)
        result_orig_img = result.orig_img     # 원본 이미지 행렬 배열
        result_orig_shape = result.orig_shape # 원본 이미지
        result_names = result.names           # 클래스 인덱스(클래스 이름 딕셔너리)
        ### 확률 데이터 정보 (result.probs)
        result_probs = result.probs.data.cpu().numpy()

        ### 가장 높은 확률의 클래스 정보
        best_index = result_probs.argmax()
        best_name = result_names[best_index]
        best_prob = result_probs[best_index]
        
        return {
            'idx': int(best_index),
            'label': str(best_name),
            'prob': float(best_prob),
        }
        return jsonify({"predictions": predictions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)