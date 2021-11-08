import base64

import numpy as np
import torch
import werkzeug.datastructures
from cv2 import cv2


# Yolo-v5를 이용한 object detection
def detect_yolo(file: werkzeug.datastructures.FileStorage) -> str:

    model = torch.hub.load('ultralytics/yolov5', 'yolov5x')

    model.conf = 0.35
    model.iou = 0.45
    model.classes = None

    # Images
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Inference
    results = model(img)

    # 이미지에 box 그리기
    results.render()

    # 이미지 불러오기
    detected_img = results.imgs[0]

    _, buffer = cv2.imencode('.png', detected_img)

    return base64.b64encode(buffer).decode('utf-8')

