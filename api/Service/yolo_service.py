from io import BytesIO

import numpy as np
import werkzeug.datastructures
from cv2 import cv2
import pydicom
from PIL import ImageFont, ImageDraw, Image
import base64, json, torch

from skimage import exposure

import matplotlib.pyplot as plt
from pydicom.pixel_data_handlers.util import apply_voi_lut, apply_modality_lut



# 정규화 등의 작업은 추후 진행
def detect_yolo(file: werkzeug.datastructures.FileStorage) -> str:

    model = torch.hub.load('ultralytics/yolov5', 'yolov5x')  # or yolov5m, yolov5l, yolov5x, custom

    model.conf = 0.45  # confidence threshold (0-1)
    model.iou = 0.45  # NMS IoU threshold (0-1)
    model.classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for persons, cats and dogs

    # Images
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Inference
    results = model(img)
    results.render()

    # Results
    # results.show()  # or .show(), .save(), .crop(), .pandas(), etc.
    # pandas = results.pandas().xyxy[0].to_json(orient="records")

    # _, buffer = cv2.imencode('.png', saved_image)

    #return json.dumps({"imgData": str(base64.b64encode(buffer))[2:-1]})

    # 이미지 불러오기
    detected_img = results.imgs[0]
    buffer = BytesIO()
    img_base64 = Image.fromarray(detected_img)
    img_base64.save(buffer, format="JPEG")
    #print(base64.b64encode(buffer.getvalue()).decode('utf-8'))  # base64 encoded image with results

    return json.dumps({"imgData": base64.b64encode(buffer.getvalue()).decode('utf-8')})

