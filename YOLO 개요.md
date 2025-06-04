# YOLO 개요

## [1] 인공지능의 분류

### 1.1.규칙기반 (Rule Based)
사람이 직접 만든 **규칙 및 수학**으로 문제를 해결  

### 1.2. 머신러닝 (Machine Learning, ML)
**데이터에서 자동으로 규칙과 패턴을 학습**해 예측·판단 수행  

## [2] 머신러닝의 분류

### 2.1. 모델(머신)에 따른 분류

> **모델이란?**  
> - 모델은 $y=mx+n$ 같은 일종의 함수.  
> - x: 입력값 , y: 출력값  
> - AI 모델이 학습한다: 데이터를 통해 적당한 가중치(m, n)을 조금씩 수정해 가는 것.


1. **딥러닝 (DeepLearning, ML)**  
    - DNN 및 DNN 계열의 모델을 사용
    - CNN, RNN, Tranformer 등
1. 서포트 벡터 머신 (SVM)
1. 의사결정 나무 (Decision Tree)    
...


### 2.2. 학습(러닝)에 따른 분류
1. **지도학습 (Supervised Learning, SL)**
    - 모델 기반 학습
    - 사람이 수집한 x, y값을 통해서 학습
    - 여기서 y를 label이라 하고 y값을 매기는 작업을 라벨링이라 함.
1. 강화학습 (Reinforcement Learning, RL)
    - 모델 기반 학습
    - 모델이 출력한 y값을 평가 (잘하면 높은 점수, 못하면 낮은 점수) 통해서 학습.
1. 비지도학습
    - 데이터 분석 분야

### 2.3. 작업에 따른 분류
1. 회귀 (Regressiono)
    - 출력값(y)가 연속형 실수
1. **분류 (Classification)**
    - 출력값(y)이 확률 분포
1. 객체 탐지 (Object Detection)
    - 입력값(x)이 이미지
    - 출력값(y)이 box 좌표, 확률 분포
1. 분할 (Segmentation)
    - 입력값(x)이 이미지
    - 출력값(y)이 box 좌표, 확률 분포, 다각형
1. 포즈 추정 (Pose Estimation)
    - 입력값(x)이 이미지
    - 출력값(y)이 box 좌표, 확률 분포, 키포인트


## [3] YOLO 란

### 3.1. YOLO (You Only Look Once)
1. 비전 분야에서 성능과 속도 모두에서 높은 성능을 보이는 알고리즘
1. 현재, [Ultralytics](https://docs.ultralytics.com/) 팀에서 주도하고 있음

### 3.2. 지원하는 Task(작업)
1. Classify (분류)
    ![alt text](https://github.com/ultralytics/docs/releases/download/0/image-classification-examples.avif)
1. Detect (객체 탐지)
    ![alt text](https://github.com/ultralytics/docs/releases/download/0/object-detection-examples.avif)
1. Segment (분할)
    ![alt text](https://github.com/ultralytics/docs/releases/download/0/instance-segmentation-examples.avif)
1. Pose (포즈)
    ![alt text](https://github.com/ultralytics/docs/releases/download/0/pose-estimation-examples.avif)


## [4] 과적합 (OverFitting)

- 모델 훈련시 훈련한 데이터에만 잘 작동하고 새로운 환경에서는 잘 작동하지 않는 현상으로 딥러닝에서 매우 자주 발생한다.
- 일반화된 모델을 잘 만드는 것이 AI 개발자의 진정한 역량이다.

### 4.1. 데이터 수집할 때 과적합 요소 제거
- 데이터를 수집할 때 모델의 학습에 방해가 되는 요소는 제거한다.
- 예를들어 고양이와 개를 분류하는 모델이 있을때, 고양이 사진 우측 상단에 빨간 점이 공통적으로 있다면 모델은 고양이 모양을 학습하는 것이 아니라 빨간 점을 통해 학습하려는 경향이 생긴다.
- 만약, 자율주행 모델을 만들 때 도로를 제외한 배경 부분은 제거하는 전처리 과정을 거치는 것도 모델의 성능 향상에 도움이 된다.

### 4.2. 데이터 수집할 때 최대한 많은 데이터 수집
- 최대한 많은 데이터를 수집하는 것이 좋다.
- 단, 다양한 환경의 데이터를 수집하는 것이 중요하다.

### 4.3. 데이터 정제
- 수집한 데이터에서 잘못된 데이터가 있다면 반드시 삭제하거나 수정한다.


### 4.4. 데이터 증강 (Augmentation)
- 많고 다양한 데이터를 수집하면 좋지만 현실적으로 어려운 경우가 많다.
- 이를 위해 수집된 데이터를 변형하여 다양한 데이터셋을 만든다.
- 예를들어, 노이즈를 추가, 회전, 반전, 색조 변경 등이 있다.
- 데이터 증강시 Task 목적에 부합하는 증강을 해야한다. 예를들어, 자율 주행 데이터의 경우 회전, 반전은 하면 안된다! (Why?)

### 4.5. 데이터셋 분할 (Split) 및 조기종료
- 똑같은 문제집을 100번 풀어보라... 당신은 어떻게 학습하게 될까?
- 수집된 데이터셋을 Train(훈련)용, Validation(검증)용 으로 나눈다. 일반적으로 8:2 비율로 나눔.
- 모델은 Train 데이터로 훈련하면서 수시로 Validation 데이터로 평가하여 모델의 평가 성능이 떨어지기 시작하면 (꼼수 부리기 시작하면) 훈련을 중단한다. 이것을 **조기 종료 (EarlyStopping)**라 함.
- Train(훈련)용 데이터와 Validation(검증)용 데이터를 나눌 때 데이터의 상관성이 적어야 한다. 비슷한 데이터가 너무 많이 섞여있으면 분할하는 의미가 없다.
    > 자율주행 데이터를 수집할 때 데이터를 너무 짧은 간격으로 수집하는 것은 좋지 않다. 이렇게 촘촘한 시간으로 수집된 데이터는 랜덤으로 분할하게 될 경우 Train 데이터와 Validation 데이터가 비슷한 것이 너무 많이 섞이게 된다.






