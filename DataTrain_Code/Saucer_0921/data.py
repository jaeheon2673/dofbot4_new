import json
import os
from params import train_params

def create_yaml_from_json():
    # train, val, test 디렉토리 경로 설정
    json_dirs = {
        'train': os.path.join(train_params.data_dir, 'train', 'images'),
        'val': os.path.join(train_params.data_dir, 'val', 'images'),
        'test': os.path.join(train_params.data_dir, 'test', 'images')
    }

    yaml_path = train_params.yaml_path

    # 첫 번째 JSON 파일을 열어서 클래스 이름과 키포인트 정보 추출
    for split, json_dir in json_dirs.items():
        json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
        
        if json_files:
            with open(os.path.join(json_dir, json_files[0]), 'r') as f:
                data = json.load(f)

            # 클래스 이름 추출
            categories = data['categories']
            class_names = [category['name'] for category in categories]

            # 키포인트 정보 추출 (COCO 형식)
            if 'annotations' in data and len(data['annotations']) > 0 and 'keypoints' in data['annotations'][0]:
                keypoints = data['annotations'][0]['keypoints']
                num_keypoints = len(keypoints) // 3  # COCO 키포인트는 (x, y, visibility) 3개씩 묶여 있음
                kpt_shape = [num_keypoints, 3]  # 키포인트 수, 각 키포인트는 (x, y, visibility)
            else:
                # 키포인트 정보가 없는 경우 기본값 설정 (필요에 따라 수정 가능)
                kpt_shape = [17, 3]  # 기본 COCO 포맷에 맞춘 값

            # YAML 파일 내용 작성 (요청한 형식에 맞춤)
            yaml_content = f"""train: {json_dirs['train']}
val: {json_dirs['val']}
test: {json_dirs['test']}

nc: {len(class_names)}  # 클래스 수
names: {class_names}  # 클래스 이름
kpt_shape: {kpt_shape}  # COCO 키포인트 형식(각 키포인트는 x, y, visibility)
"""

            # YAML 파일 저장
            with open(yaml_path, 'w') as f:
                f.write(yaml_content)

            print(f"YAML 파일이 생성되었습니다: {yaml_path}")
            return  # YAML 파일이 생성되면 함수 종료
        else:
            print(f"{split} 폴더에 JSON 파일을 찾을 수 없습니다.")
    
    print("모든 폴더에서 JSON 파일을 찾을 수 없습니다.")

# 실행 코드
create_yaml_from_json()
