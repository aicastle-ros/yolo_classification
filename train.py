# 사전 훈련된 모델 - n: nano, s: small, m: medium, l: large, x: extra large
pretrained_model_name = "yolo11n-cls.pt"  

# 데이터셋 경로 설정
collect_dir = 'dataset/collect'
yolo_format_dir = 'dataset/yolo'

# 모델 훈련 결과가 저장될 위치 (default: 'runs/classify' )
results_dir = 'runs/classify'

# 기본 train/val 분할 비율
train_val_split_ratio = 0.8  

# 훈련 하이퍼파라미터 설정
train_args = {
    'data': yolo_format_dir,
    'project': results_dir,
    'epochs': 50,    # 최대 에포크
    'patience': 10,  # 조기 종료를 위한 patience
    'save_period': 5 # 모델 가중치 저장 빈도 (-1:비활성)
    'batch': 16,     # 모델 가중치를 업데이트할 때 참고할 데이터의 묶음 수 (-1:자동)
    'imgsz': 128,    # 입력할 때 조정할 이미지 크기
    'plots': True,   # 훈련 결과 시각화 저장
    ### augmetation
    'augment': True,      # 데이터 증강 사용
    'auto_augment': None, # 자동 증강 끄기 (수동 설정)
    'hsv_h': 0.015, # 색조 조정
    'hsv_s': 0.7,   # 채도 조정
    'hsv_v': 0.4,   # 밝기 조정
    'degrees': 0.0, # 회전 각도 조정  ! 중요 - 자율주행에서는 사용하지 않는 것이 좋음
    'translate': 0.1, # 수평/수직 이동
    'scale': 0.5,   # 크기 조정  
    'shear': 0.0,   # 전단 변형
    'perspective': 0.0,  # 관점 변형
    'flipud': 0.0,  # 상하 반전  ! 중요 - 자율주행에서는 사용하지 않는 것이 좋음
    'fliplr': 0.0,  # 좌우 반전  ! 중요 - 자율주행에서는 사용하지 않는 것이 좋음
    'bgr': 0.0,     # BGR 색상 공간 변환
    'mosaic': 0.0,  # 모자이크 증강 ! 중요 - 자율주행에서는 사용하지 않는 것이 좋음
    'mixup': 0.0,   # MixUp 증강  ! 중요 - 자율주행에서는 사용하지 않는 것이 좋음
    'cutmix': 0.0,  # CutMix 증강 ! 중요 - 자율주행에서는 사용하지 않는 것이 좋음
    # 'copy_paste': 0.0, # 복사-붙여넣기 : segmetation에서만 적용 됨.
    # 'copy_paste_mode': 'flip', # 복사-붙여넣기 모드 : segmetation에서만 적용 됨.
    'erasing': 0.4, # 지우기 증강 - classify 모드에서만 작동됨.
}

###################################################################

import os
import shutil
import random
import glob
import torch
from ultralytics import YOLO

def check_cuda():
    if torch.cuda.is_available():
        device_idx = torch.cuda.current_device()
        device_name = torch.cuda.get_device_name(device_idx)
        total_mem = torch.cuda.get_device_properties(device_idx).total_memory
        print(f"CUDA is available. Device index: {device_idx}")
        print(f"Device name: {device_name}")
        print(f"Total memory (bytes): {total_mem}")
    else:
        print("CUDA is not available. Training will run on CPU.")
    
def train_val_split(train_val_split_ratio=0.8):
    # collect 폴더가 존재하는지 확인
    if not os.path.exists(collect_dir):
        print(f"Error: {collect_dir} does not exist.")
        return

    # 각 클래스 폴더를 순회
    class_dirs = [d for d in os.listdir(collect_dir) 
                  if os.path.isdir(os.path.join(collect_dir, d))]

    if not class_dirs:
        print(f"Error: not found any class directories in {collect_dir}.")
        return
    
    print(f"Found class directories: {class_dirs}")

    if os.path.exists(yolo_format_dir):
        shutil.rmtree(yolo_format_dir)  # 기존 yolo_format 폴더 삭제

    os.makedirs(os.path.join(yolo_format_dir, 'train'), exist_ok=True)
    os.makedirs(os.path.join(yolo_format_dir, 'val'), exist_ok=True)

    for class_name in class_dirs:
        class_path = os.path.join(collect_dir, class_name)
        
        # 이미지 파일들 수집 (jpg, jpeg, png, bmp 등)
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.JPG', '*.JPEG', '*.PNG', '*.BMP']:
            image_files.extend(glob.glob(os.path.join(class_path, ext)))
        
        if not image_files:
            print(f"Warning: {class_name} does not contain any image files.")
            continue

        # 이미지 파일들을 랜덤하게 섞기
        random.shuffle(image_files)
        
        # train/val 분할 계산
        total_files = len(image_files)
        train_count = int(total_files * train_val_split_ratio)
        
        train_files = image_files[:train_count]
        val_files = image_files[train_count:]
        
        print(f"{class_name}: total {total_files}, train {len(train_files)}, val {len(val_files)}")
        
        # train 폴더에 클래스 폴더 생성
        train_class_dir = os.path.join(yolo_format_dir, 'train', class_name)
        os.makedirs(train_class_dir, exist_ok=True)
        
        # val 폴더에 클래스 폴더 생성
        val_class_dir = os.path.join(yolo_format_dir, 'val', class_name)
        os.makedirs(val_class_dir, exist_ok=True)
        
        # train 파일들에 대해 symbolic link 생성
        for file_path in train_files:
            file_name = os.path.basename(file_path)
            src_path = os.path.abspath(file_path)
            dst_path = os.path.join(train_class_dir, file_name)
            os.symlink(src_path, dst_path)
        
        # val 파일들에 대해 symbolic link 생성
        for file_path in val_files:
            file_name = os.path.basename(file_path)
            src_path = os.path.abspath(file_path)
            dst_path = os.path.join(val_class_dir, file_name)
            os.symlink(src_path, dst_path)

    print(f"Train/val split completed. Data is in {yolo_format_dir}.")

if __name__ == "__main__":
    check_cuda()
    train_val_split(train_val_split_ratio=train_val_split_ratio)

    model = YOLO(f"models/pretrained/{pretrained_model_name}")
    model.train(**train_args)