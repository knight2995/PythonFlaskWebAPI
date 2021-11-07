import base64
import json
import torch

import numpy as np
import werkzeug.datastructures
from cv2 import cv2


# 정규화 등의 작업은 추후 진행
def detect_yolo(file: werkzeug.datastructures.FileStorage) -> str:

    model = torch.hub.load('ultralytics/yolov5', 'yolov5x')

    model.conf = 0.35  # confidence threshold (0-1)
    model.iou = 0.45  # NMS IoU threshold (0-1)
    model.classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs

    # Images
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Inference
    results = model(img)
    results.render()


    # 이미지 불러오기
    detected_img = results.imgs[0]

    _, buffer = cv2.imencode('.png', detected_img)

    return base64.b64encode(buffer).decode('utf-8')

