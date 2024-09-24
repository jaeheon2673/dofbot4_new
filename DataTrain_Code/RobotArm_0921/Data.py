import os
import json

def create_yaml(data_dir, yaml_path):
    # 기본 클래스 정의 (직접 정의)
    default_class_names = ['grasping_cup', 'flipping_cup', 'flipped_cup']
    class_names = set(default_class_names)  # 중복을 방지하기 위해 집합으로 저장

    # train, val, test 경로 정의
    train_path = os.path.join(data_dir, 'train', 'images')
    val_path = os.path.join(data_dir, 'val', 'images')
    test_path = os.path.join(data_dir, 'test', 'images')

    # JSON 파일에서 클래스 이름과 키포인트 정보 추출
    for split in ['train', 'val', 'test']:
        img_dir = os.path.join(data_dir, split, 'images')
        json_files = [f for f in os.listdir(img_dir) if f.endswith('.json')]
        
        if json_files:
            for json_file in json_files:
                json_path = os.path.join(img_dir, json_file)
                with open(json_path, 'r') as f:
                    data = json.load(f)

                # # JSON에서 클래스 이름 추출
                # categories = data.get('categories', [])
                # class_names.update([category['name'] for category in categories])

                # 키포인트 정보 추출 (첫 번째 파일에서만 필요)
                if 'annotations' in data and len(data['annotations']) > 0 and 'keypoints' in data['annotations'][0]:
                    keypoints = data['annotations'][0]['keypoints']
                    num_keypoints = len(keypoints) // 3  # COCO 키포인트는 (x, y, visibility) 3개씩 묶여 있음
                    kpt_shape = [num_keypoints, 3]  # 키포인트 수, 각 키포인트는 (x, y, visibility)
                    break
        else:
            print(f"{split} 폴더에 JSON 파일을 찾을 수 없습니다.")
    
    # 키포인트 정보가 없다면 기본값 설정
    if 'kpt_shape' not in locals():
        kpt_shape = [7, 3]  # COCO 기본 포맷

    # YAML 파일 내용 구성
    yaml_content = f"""train: {train_path}
val: {val_path}
test: {test_path}

nc: {len(class_names)}  # 클래스 수
names: {list(class_names)}  # 클래스 이름
kpt_shape: {kpt_shape}  # COCO 키포인트 형식(각 키포인트는 x, y, visibility)
"""
    # YAML 파일 생성
    with open(yaml_path, 'w') as f:
        f.write(yaml_content)

    print(f"YAML 파일이 생성되었습니다: {yaml_path}")

# 실행 예시 (robot_arm.yaml으로 변경)
data_dir = './data'  # 데이터 디렉토리
yaml_path = './robot_arm.yaml'  # 생성할 YAML 파일 경로
create_yaml(data_dir, yaml_path)
