from ultralytics import YOLO
from params import train_params
import torch

# CUDA 사용 여부 설정
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# 모델 로드 및 설정
try:
    model = YOLO(train_params.model).to(device)
    print(f"Model {train_params.model} successfully loaded.")
except Exception as e:
    print(f"Error loading model: {e}")
    raise

# 모델 학습 및 검증 과정 함수화
def train_and_validate(model, device, train_params):
    # 학습 반복 (에포크마다)
    for epoch in range(train_params.epochs):
        print(f"\nStarting Epoch {epoch + 1}/{train_params.epochs}")
        
        # Train step
        try:
            results_train = model.train(
                data=train_params.yaml_path,
                epochs=1,  # 한 번의 에포크 진행
                imgsz=train_params.img_size,
                batch=train_params.batch_size,
                project=train_params.project,
                name=train_params.name,
                save_period=train_params.save_period,
                device=device
            )

            # Train 결과 출력
            train_map50 = results_train.box.map50
            train_map95 = results_train.box.map
            print(f"Epoch {epoch + 1}: Train mAP@0.5: {train_map50:.4f}, Train mAP@0.5:0.95: {train_map95:.4f}")

        except Exception as e:
            print(f"Error during training at epoch {epoch + 1}: {e}")
            continue

        # Validation step
        try:
            results_val = model.val(
                data=train_params.yaml_path,
                batch=train_params.batch_size,
                imgsz=train_params.img_size,
                device=device
            )

            # Validation 결과 출력
            val_map50 = results_val.box.map50
            val_map95 = results_val.box.map
            print(f"Epoch {epoch + 1}: Validation mAP@0.5: {val_map50:.4f}, Validation mAP@0.5:0.95: {val_map95:.4f}")

        except Exception as e:
            print(f"Error during validation at epoch {epoch + 1}: {e}")
            continue

# 모델 학습 및 검증 실행
train_and_validate(model, device, train_params)

# 테스트 단계 (모든 에포크가 끝난 후)
try:
    print("\nStarting final model testing...")
    results_test = model.val(
        data=train_params.yaml_path,
        batch=train_params.batch_size,
        imgsz=train_params.img_size,
        device=device
    )

    # Test 결과 출력
    test_map50 = results_test.box.map50
    test_map95 = results_test.box.map
    print(f"Final Test Results - mAP@0.5: {test_map50:.4f}, mAP@0.5:0.95: {test_map95:.4f}")

except Exception as e:
    print(f"Error during testing: {e}")

print("모델 학습 및 테스트 완료")
