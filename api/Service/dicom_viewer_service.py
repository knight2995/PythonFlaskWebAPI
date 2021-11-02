import numpy as np
import werkzeug.datastructures
from cv2 import cv2
import pydicom
from PIL import ImageFont, ImageDraw, Image
import base64, json

from skimage import exposure

import matplotlib.pyplot as plt
from pydicom.pixel_data_handlers.util import apply_voi_lut, apply_modality_lut


# 틀만 잡아놓기
# 정규화 등의 작업은 추후 진행
def convert_dicom_image_to_png(file: werkzeug.datastructures.FileStorage) -> str:
    window_center = 50
    window_width = 350

    ds = pydicom.read_file(file)

    pixel_array = ds.pixel_array  # dicom image
    Rescale_slope = ds.RescaleSlope  # dicom header (Rescale slope)
    Rescale_intercept = ds.RescaleIntercept  # dicom header (Rescale intercept)
    Window_center = ds.WindowCenter  # dicom header (Window center)
    Window_width = ds.WindowWidth  # dicom header (Window width)
    Photometric_interpretation = ds.PhotometricInterpretation  # dicom header (Photometric interpretation)

    #windowed = apply_voi_lut(ds.pixel_array, ds)

    image = exposure.equalize_adapthist(pixel_array)
    saved_image = 255 * image  # Now scale by 255
    saved_image = saved_image.astype(np.uint8)

    _, buffer = cv2.imencode('.png', saved_image)
    print(len(buffer))

    return json.dumps({"imgData": str(base64.b64encode(buffer))[2:-1]})

