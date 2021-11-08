import base64
import json

import numpy as np
import pydicom
import werkzeug.datastructures
from cv2 import cv2
from skimage import exposure


# dicom to png
# Not Implemented HU 범위에 따른 보정
def convert_dicom_image_to_png(file: werkzeug.datastructures.FileStorage, _type: str):
    window_center = 50
    window_width = 350

    ds: pydicom.FileDataset = pydicom.read_file(file)

    pixel_array = ds.pixel_array  # dicom image

    image = exposure.equalize_adapthist(pixel_array)

    saved_image = 255 * image  # Now scale by 255
    saved_image = saved_image.astype(np.uint8)

    _, buffer = cv2.imencode('.png', saved_image)

    # 태그 정보 파싱
    if _type == 'standard':
        tags = get_tags(ds)
    else:
        tags = get_tags_all(ds)

    return base64.b64encode(buffer).decode('utf-8'), tags


def get_tags(ds: pydicom.FileDataset) -> dict:

    tags = dict()

    tags['PatientName'] = str(ds.PatientName) if hasattr(ds, 'PatientName') else ''
    tags['PatientID'] = str(ds.PatientID) if hasattr(ds, 'PatientID') else ''
    tags['PatientBirthDate'] = str(ds.PatientBirthDate) if hasattr(ds, 'PatientBirthDate') else ''
    tags['PatientSex'] = str(ds.PatientSex) if hasattr(ds, 'PatientSex') else ''
    tags['PatientAge'] = str(ds.PatientAge) if hasattr(ds, 'PatientAge') else ''

    tags['StudyDate'] = str(ds.StudyDate) if hasattr(ds, 'StudyDate') else ''
    tags['StudyTime'] = str(ds.StudyTime) if hasattr(ds, 'StudyTime') else ''
    tags['StudyID'] = str(ds.StudyID) if hasattr(ds, 'StudyID') else ''
    tags['Modality'] = str(ds.Modality) if hasattr(ds, 'Modality') else ''
    tags['StudyDescription'] = str(ds.StudyDescription) if hasattr(ds, 'StudyDescription') else ''

    tags['SeriesDate'] = str(ds.SeriesDate) if hasattr(ds, 'SeriesDate') else ''
    tags['SeriesTime'] = str(ds.SeriesTime) if hasattr(ds, 'SeriesTime') else ''
    tags['SeriesDescription'] = str(ds.SeriesDescription) if hasattr(ds, 'SeriesDescription') else ''

    return tags


def get_tags_all(ds: pydicom.FileDataset) -> list:
    tags = list()

    data = str(ds)

    _, file_meta, meta_tags = data.split('-------------------------------')

    for v in file_meta.splitlines():
        if len(v) == 0:
            continue

        tag = list()
        tag.append({'(Group,Element)': v[:12]})
        tag.append({'(TAG Description)': v[13:47]})
        tag.append({'(Value)': v[49:]})
        tags.append(tag)

    # Simplify implement
    for v in meta_tags.splitlines()[1:]:
        group_element = v[:v.find(')') + 1]
        tag_description = v[v.find(')') + 2:v.find(':') - 2]
        value = v[v.find(':') - 2:]

        tag = list()
        tag.append({'(Group,Element)': group_element})
        tag.append({'(TAG Description)': tag_description})
        tag.append({'(Value)': value})
        tags.append(tag)

    return tags
