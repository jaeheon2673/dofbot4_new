from ultralytics import YOLO
from params import train_params
import torch

# CUDA 사용 여부 설정
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# 모델 로드 및 설정
model = YOLO(train_params.model).to(device)

# 사용자 정의 데이터셋으로 모델 학습
for epoch in range(train_params.epochs):
    print(f"Epoch {epoch + 1}/{train_params.epochs}")
    
    # 1. Train step
    results_train = model.train(
        data=train_params.yaml_path,
        epochs=1,
        imgsz=train_params.img_size,
        batch=train_params.batch_size,
        project=train_params.project,
        name=train_params.name,
        save_period=train_params.save_period,
        device=device
    )
    
    # Train 결과 출력 (최신 API 반영)
    train_map50 = results_train.box.map50
    train_map95 = results_train.box.map
    train_map75 = results_train.box.map75
    train_maps = results_train.box.maps
    
    print(f"Train mAP@0.5: {train_map50}, Train mAP@0.5:0.95: {train_map95}")
    print(f"Train mAP@0.75: {train_map75}, Train mAPs: {train_maps}")

    # 2. Validation step
    results_val = model.val(
        data=train_params.yaml_path,
        batch=train_params.batch_size,
        imgsz=train_params.img_size,
        device=device
    )
    
    # Validation 결과 출력 (최신 API 반영)
    val_map50 = results_val.box.map50
    val_map95 = results_val.box.map
    val_map75 = results_val.box.map75
    val_maps = results_val.box.maps
    
    print(f"Validation mAP@0.5: {val_map50}, Validation mAP@0.5:0.95: {val_map95}")
    print(f"Validation mAP@0.75: {val_map75}, Validation mAPs: {val_maps}")

# 마지막 에포크 후 Test
results_test = model.val(
    data=train_params.yaml_path,
    batch=train_params.batch_size,
    imgsz=train_params.img_size,
    device=device
)

# Test 결과 출력 (최신 API 반영)
test_map50 = results_test.box.map50
test_map95 = results_test.box.map
test_map75 = results_test.box.map75
test_maps = results_test.box.maps

print(f"Test mAP@0.5: {test_map50}, Test mAP@0.5:0.95: {test_map95}")
print(f"Test mAP@0.75: {test_map75}, Test mAPs: {test_maps}")

print("모델 학습 완료")
