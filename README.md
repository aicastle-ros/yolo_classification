# Yolo Classification

[**YOLO**](https://docs.ultralytics.com/)를 활용하여 jetson nano에서 차량의 카메라 센서로 딥러닝 자율주행 모델을 구현합니다.

## [1] Installation - jetson nano (ubuntu 20.04)


### 1.1. 스왑 메모리 확장 (옵션)
```bash
# 원하는 크기 만큼 빈 파일 생성 (8G)
sudo fallocate -l 8G /swapfile
# 파일 권한 설정
sudo chmod 600 /swapfile
# 스왑 영역으로 포맷하기
sudo mkswap /swapfile
# 스왑 활성화하기
sudo swapon /swapfile
# 부팅 시 자동으로 스왑 켜기
grep -qxF '/swapfile none swap sw 0 0' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 1.2. 도커 권한 부여
    
```bash
sudo usermod -aG docker "$USER"
```
- 실행 후 재부팅 필요
    

### 1.3. 레포지토리 클론
```bash
cd ~
git clone https://github.com/aicastle-ros/yolo_classification.git
cd yolo_classification
```

### 1.4. 설치 (도커 빌드)
```bash
docker build -t yolo:latest .
```

## [2] Train (`train.py`)

### 2.1. 훈련 시작하기
```bash
docker run -it --rm \
    --name yolo_train \
    --ipc=host \
    -u $(id -u):$(id -g) \
    --runtime=nvidia \
    -v /home/jetson/yolo_classification:/workspace \
    yolo:latest \
    python3 train.py
```


### 2.2. 분류 모델 종류

[**YOLO docs**](https://docs.ultralytics.com/tasks/classify/#models)

| 종류 | 파일명 |
| --- | ----- |
| n (nano)   | `yolo11n-cls.pt` |
| s (small)  | `yolo11s-cls.pt` |
| m (medium) | `yolo11m-cls.pt` |
| l (large)  | `yolo11l-cls.pt` |


### 2.3. 데이터셋
- `collect_dir`: 수집한 데이터
    ```
    collect_dir
    ├── class 1
    │   ├── class1-001.jpg
    │   ├── class1-002.jpg
    │   ├── class1-003.jpg
    │   ...
    ├── class 2
    │   ├── class2-001.jpg
    │   ├── class2-002.jpg
    │   ├── class2-003.jpg
    │   ...
    ├── class 3
    │   ├── class3-001.jpg
    │   ├── class3-002.jpg
    │   ├── class3-003.jpg
    │   ...
    ```
- `yolo_format_dir`: 수집한 데이터를 train 과 val 로 분할
    ```
    yolo_format_dir
    ├── train
    │    ├── class 1
    │    │   ├── class1-001.jpg
    │    │   ├── class1-002.jpg
    │    │   ...
    │    ├── class 2
    │    │   ├── class2-001.jpg
    │    │   ├── class2-002.jpg
    │    │   ...
    │    ├── class 3
    │    │   ├── class3-001.jpg
    │    │   ├── class3-002.jpg
    │       ...
    └── val
            ├── class 1
            │   ├── class1-003.jpg
            │   ├── class1-004.jpg
            │   ...
            ├── class 2
            │   ├── class2-003.jpg
            │   ├── class2-004.jpg
            │   ...
            ├── class 3
            │   ├── class3-003.jpg
            │   ├── class3-004.jpg
               ...
    ```
- `train_val_split_ratio`: train과 val로 분할 비율
    > 만약, 0.8이면, 8:2 로 나누어짐

### 2.4. 훈련 하이퍼파라미터 설정

#### [**일반 하이퍼파라미터**](https://docs.ultralytics.com/modes/train/#train-settings)

- `epochs`: 최대 에포크 (훈련 시 전체 데이터셋을 몇 번 반복할지 설정)
- `patience`: 성능 개선이 없을 경우 조기 종료를 위한 인내 에포크 수 (연속으로 성능 향상이 없으면 훈련을 멈춤)
- `batch`: 배치 크기 (한 번에 네트워크에 입력으로 넣는 이미지 개수; 메모리 및 학습 속도에 영향)
- `imgsz`: 입력 이미지 크기 (훈련 시 네트워크에 공급할 이미지의 한 변 길이; 예: 128 → 128×128 픽셀)
- `plots`: 훈련 결과 시각화를 저장할지 여부 (True면 loss/precision/recall 등 곡선을 그래프로 그려 파일로 저장)
- `augment`: 데이터 증강 사용 여부 (True면 아래에 설정한 여러 증강 기법을 적용)

#### [**증강 하이퍼파라미터**](https://docs.ultralytics.com/guides/yolo-data-augmentation/)
- `auto_augment`: 자동 증강 사용 설정 (None이면 자동 증강 모듈을 끄고, 직접 설정값을 사용)
- `hsv_h`: 색조(Hue) 조정 비율 (0.015면 픽셀마다 ±1.5% 정도 색조를 무작위로 변경)
- `hsv_s`: 채도(Saturation) 조정 비율 (0.7이면 채도를 최대 ±70%까지 무작위로 변경)
- `hsv_v`: 명도(Value) 조정 비율 (0.4면 밝기를 최대 ±40%까지 무작위로 변경)
- `degrees`: 회전 각도 조정 범위 (0.0이면 회전 미사용; 자율주행 데이터에서는 회전 보통 사용하지 않음)
- `translate`: 수평/수직 이동 비율 (0.1이면 이미지 폭/높이의 ±10% 범위 내에서 랜덤 이동)
- `scale`: 크기 조정 비율 (0.5면 이미지 크기를 50%~150% 사이에서 무작위로 조정)
- `shear`: 전단 변형 비율 (0.0이면 전단 변형 미사용)
- `perspective`: 원근(투시) 변형 강도 (0.0이면 원근 변형 미사용)
- `flipud`: 상하 반전 확률 (0.0이면 상하 뒤집기 미사용; 자율주행에서는 사용하지 않는 것이 좋음)
- `fliplr`: 좌우 반전 확률 (0.0이면 좌우 뒤집기 미사용; 자율주행에서는 사용하지 않는 것이 좋음)
- `bgr`: BGR 색상 공간 변환 확률 (0.0이면 색상 채널 순서 변경 미사용)
- `mosaic`: 모자이크 증강 확률 (0.0이면 모자이크 미사용; 자율주행에서는 사용하지 않는 것이 좋음)
- `mixup`: MixUp 증강 확률 (0.0이면 MixUp 미사용; 자율주행에서는 사용하지 않는 것이 좋음)
- `cutmix`: CutMix 증강 확률 (0.0이면 CutMix 미사용; 자율주행에서는 사용하지 않는 것이 좋음)
- `erasing`: 랜덤 지우기(Erasing) 증강 확률 (0.4면 이미지의 일부를 최대 40% 영역까지 무작위로 지워서 학습 데이터 다양성 증가)

### 2.5. 훈련 모델 결과

- 분류 모델의 경우 `runs/classify/train<idx>` 형태의 폴더에 저장 됨
- 모델 가중치 파일은 `runs/classify/train<idx>/weights` 폴더에 저장 됨.
    - `best.pt`: val 에서 가장 높은 훈련 결과를 기록한 모델 가중치치
    - `last.pt` : 모델 훈련이 (조기) 종료 된 시점의 마지막 모델 가중치



## [3] Serve (`server.py`)

### 3.1. 서빙 시작하기
```bash
docker run -it --rm \
    --name yolo_server \
    --ipc=host \
    -p 5000:5000 \
    --runtime=nvidia \
    -v /home/jetson/yolo_classification:/workspace \
    yolo:latest \
    python3 server.py
```

### 3.2. 서빙할 모델 경로

`MODEL_PATH` 환경 변수로 지정합니다. 
