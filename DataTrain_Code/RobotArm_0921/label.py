import os
import json
from PIL import Image  # 이미지 크기를 자동으로 얻기 위해 사용

def convert_coco_to_yolo(json_file, img_file, output_dir):
    """
    COCO 형식의 JSON 파일을 YOLO 형식의 라벨 파일로 변환
    json_file: COCO 형식의 어노테이션 파일
    img_file: 이미지 파일 경로
    output_dir: YOLO 라벨을 저장할 디렉토리
    class_map: 클래스 이름을 클래스 ID로 변환하는 맵
    """
    # 이미지 크기를 불러오기
    with Image.open(img_file) as img:
        img_width, img_height = img.size

    # JSON 파일 읽기
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 출력 디렉토리 생성 (없으면 생성)
    os.makedirs(output_dir, exist_ok=True)

    # 어노테이션 정보 변환
    for annotation in data['annotations']:
        img_file_name = os.path.splitext(os.path.basename(img_file))[0] + ".txt"
        bbox = annotation['bbox']

        # 클래스 이름을 ID로 변환 (class_map을 통해 클래스 ID 매핑)
        class_id = annotation['category_id']

        # 바운딩 박스 YOLO 형식으로 변환
        x, y, w, h = bbox
        x_center = (x + w / 2) / img_width  # x 좌표 정규화
        y_center = (y + h / 2) / img_height  # y 좌표 정규화
        w = w / img_width  # 너비 정규화
        h = h / img_height  # 높이 정규화

        # 키포인트 처리
        keypoints = annotation.get('keypoints', [])
        keypoint_data = []
        for i in range(0, len(keypoints), 3):
            x_kp = keypoints[i] / img_width  # 키포인트 x 좌표 정규화
            y_kp = keypoints[i + 1] / img_height  # 키포인트 y 좌표 정규화
            visibility = keypoints[i + 2]  # visibility 값은 정규화할 필요 없음
            keypoint_data.extend([x_kp, y_kp, visibility])

        # 라벨을 YOLO 형식으로 저장
        label_path = os.path.join(output_dir, img_file_name)
        with open(label_path, 'w') as label_file:
            label_file.write(f"{class_id} {x_center} {y_center} {w} {h} " + ' '.join(map(str, keypoint_data)) + "\n")

# def create_class_map(json_file):
#     """
#     JSON 파일에서 카테고리 정보를 읽어 클래스 이름과 클래스 ID의 매핑을 생성
#     json_file: COCO 형식의 어노테이션 파일
#     """
#     with open(json_file, 'r') as f:
#         data = json.load(f)

#     categories = data['categories']
#     class_map = {category['id']: idx for idx, category in enumerate(categories)}
    
#     return class_map

# 데이터셋 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
train_images_dir = os.path.join(base_dir, 'data/train/images')
train_labels_dir = os.path.join(base_dir, 'data/train/labels')
val_images_dir = os.path.join(base_dir, 'data/val/images')
val_labels_dir = os.path.join(base_dir, 'data/val/labels')

# train 폴더에서 첫 번째 JSON 파일을 찾아 클래스 맵 생성
sample_json_path = os.path.join(train_images_dir, os.listdir(train_images_dir)[0].replace('.png', '.json'))
# class_map = create_class_map(sample_json_path)

# 모든 train 이미지와 JSON 파일을 변환하여 라벨 생성
for img_file in os.listdir(train_images_dir):
    if img_file.endswith('.png'):  # 이미지 파일에 대해서만 처리
        json_file = img_file.replace('.png', '.json')  # JSON 파일 이름 유추
        json_path = os.path.join(train_images_dir, json_file)
        img_path = os.path.join(train_images_dir, img_file)

        # JSON 파일이 있는지 확인 후 라벨 변환
        if os.path.exists(json_path):
            convert_coco_to_yolo(json_path, img_path, train_labels_dir)

# 모든 val 이미지와 JSON 파일을 변환하여 라벨 생성
for img_file in os.listdir(val_images_dir):
    if img_file.endswith('.png'):  # 이미지 파일에 대해서만 처리
        json_file = img_file.replace('.png', '.json')  # JSON 파일 이름 유추
        json_path = os.path.join(val_images_dir, json_file)
        img_path = os.path.join(val_images_dir, img_file)

        # JSON 파일이 있는지 확인 후 라벨 변환
        if os.path.exists(json_path):
            convert_coco_to_yolo(json_path, img_path, val_labels_dir)
