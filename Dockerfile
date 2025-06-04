# 베이스 이미지
FROM ultralytics/ultralytics:latest-jetson-jetpack4

WORKDIR /workspace

RUN pip install flask