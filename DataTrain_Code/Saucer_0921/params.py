# params.py

import os

class TrainParams:
    def __init__(self):
        # 베이스 디렉토리 설정
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 데이터셋 경로 설정
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.train_data = os.path.join(self.data_dir, 'train/images')
        self.val_data = os.path.join(self.data_dir, 'val/images')
        self.test_data = os.path.join(self.data_dir, 'test/images')
        self.yaml_path = os.path.join(self.data_dir, 'Saucer.yaml')

        # 결과 저장 경로
        self.outs_dir = os.path.join(self.base_dir, 'outs')
        os.makedirs(self.outs_dir, exist_ok=True)
        self.project = self.outs_dir  # 저장 폴더 경로
        self.name = 'Sweight'  # 결과 파일 이름

        # 학습 설정 파라미터
        self.model = 'yolov8s-pose.pt'  # YOLOv8s 모델 설정 파일
        self.epochs = 100  # 학습할 에포크 수
        self.img_size = 640  # 입력 이미지 크기
        self.batch_size = 8  # 배치 크기
        self.save_period = 1  # 매 에포크마다 가중치 저장
        self.patience = 10  # Early stopping: 성능 개선이 없을 경우 10 에포크 후 중지
        self.optimizer = 'AdamW'  # 최적화 알고리즘
        self.lr0 = 5e-6  # 초기 학습률
        self.lrf = 0.01  # 마지막 학습률
        self.momentum = 0.9  # 모멘텀
        self.weight_decay = 5e-4  # 가중치 감쇠
        self.augment = True  # 데이터 증강 적용 여부

# 파라미터 설정 객체를 인스턴스화
train_params = TrainParams()
