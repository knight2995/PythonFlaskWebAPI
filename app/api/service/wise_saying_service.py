import numpy as np
import werkzeug.datastructures
from cv2 import cv2
from PIL import ImageFont, ImageDraw, Image
import base64, json


def make_wise_saying(file: werkzeug.datastructures.FileStorage, text: str) -> str:
    # load Image
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # resize image
    # width, height, channels
    img_height, img_width, _ = img.shape
    if img_width > 512 or img_height > 512:
        ratio = max(img_width, img_height) / 512
        img = cv2.resize(img, dsize=(0, 0), fx=1 / ratio, fy=1 / ratio, interpolation=cv2.INTER_AREA)

    # convert to grayScale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # make 3-channels grayscale
    img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    img[:, :, 0] = gray
    img[:, :, 1] = gray
    img[:, :, 2] = gray

    wise_saying_image = make_wise_saying_image(img, text)

    _, buffer = cv2.imencode('.jpg', wise_saying_image)

    return json.dumps({"imgData": str(base64.b64encode(buffer))[2:-1]})


def make_wise_saying_image(img: np.ndarray, text: str) -> np.ndarray:
    # width, height, channels
    img_height, img_width, img_channels = img.shape

    # 텍스트 출력에 필요한 최대 가로 길이 확인
    lines = text.splitlines()
    max_text_line_length = max(map(lambda x: len(x), lines))

    wise_saying_image = np.zeros((max(img_height, 20 * len(lines)),
                                  img_width + 60 + max_text_line_length * 20, 3), np.uint8)

    b, g, r, a = 255, 255, 255, 0
    font_path = "fonts/gulim.ttc"
    font = ImageFont.truetype(font_path, 20)
    img_pil = Image.fromarray(wise_saying_image)
    draw = ImageDraw.Draw(img_pil)
    draw.text((30 + img_width, 30), text, font=font, fill=(b, g, r, a))

    wise_saying_image = np.array(img_pil)

    wise_saying_image_height, _, _ = wise_saying_image.shape

    if img.shape[0] % 2 == 0:

        wise_saying_image[wise_saying_image_height // 2 - img_height // 2:
                          wise_saying_image_height // 2 + img_height // 2, 0: img_width] = img
    else:
        wise_saying_image[wise_saying_image_height // 2 - img_height // 2:
                          wise_saying_image_height // 2 + img_height // 2 + 1, 0: img_width] = img

    return wise_saying_image
