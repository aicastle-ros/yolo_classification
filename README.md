# Yolo Classification

[**YOLO**](https://docs.ultralytics.com/)를 활용하여 차량의 카메라 센서로 딥러닝 자율주행 모델을 구현합니다.

## [1] Installation

### jetson nano (ubuntu 20.04)에 설치

```bash
pip install ultralytics  # ultralytics yolo 설치
sudo fallocate -l 8G /swapfile  # 원하는 크기 만큼 빈 파일 생성
sudo chmod 600 /swapfile  # 파일 권한 설정
sudo mkswap /swapfile # 스왑 영역으로 포맷하기 
sudo swapon /swapfile # 스왑 활성화하기
grep -qxF '/swapfile none swap sw 0 0' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab  # 부팅 시 자동으로 스왑 켜기
```

### codespaces에 설치
```bash
sudo apt-get update
sudo apt-get install -y libgl1
pip3 install ultralytics
```


## [2] Train

```bash
python3 train.py
```