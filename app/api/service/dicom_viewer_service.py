import numpy as np
import werkzeug.datastructures
from cv2 import cv2
import pydicom
from PIL import ImageFont, ImageDraw, Image
import base64, json
import re
from skimage import exposure

import matplotlib.pyplot as plt
from pydicom.pixel_data_handlers.util import apply_voi_lut, apply_modality_lut


# 틀만 잡아놓기
# 정규화 등의 작업은 추후 진행
def convert_dicom_image_to_png(file: werkzeug.datastructures.FileStorage, type: str) -> str:
    window_center = 50
    window_width = 350

    ds: pydicom.FileDataset = pydicom.read_file(file)

    pixel_array = ds.pixel_array  # dicom image
    # Rescale_slope = ds.RescaleSlope  # dicom header (Rescale slope)
    # Rescale_intercept = ds.RescaleIntercept  # dicom header (Rescale intercept)
    # Window_center = ds.WindowCenter  # dicom header (Window center)
    # Window_width = ds.WindowWidth  # dicom header (Window width)
    # Photometric_interpretation = ds.PhotometricInterpretation  # dicom header (Photometric interpretation)

    # windowed = apply_voi_lut(ds.pixel_array, ds)

    image = exposure.equalize_adapthist(pixel_array)

    saved_image = 255 * image  # Now scale by 255
    saved_image = saved_image.astype(np.uint8)

    _, buffer = cv2.imencode('.png', saved_image)

    if type == 'standard':
        tags = get_tags(ds)
    elif type == 'all':
        tags = get_tags_all(ds)


    return json.dumps({"imgData": str(base64.b64encode(buffer))[2:-1], 'tags': tags})


def get_tags(ds: pydicom.FileDataset) -> dict:
    tags = dict()


    tags['PatientName'] = str(ds.PatientName)
    tags['PatientID'] = str(ds.PatientID)
    tags['PatientBirthDate'] = str(ds.PatientBirthDate)
    tags['PatientSex'] = str(ds.PatientSex)
    tags['PatientAge'] = str(ds.PatientAge)

    tags['StudyDate'] = str(ds.StudyDate)
    tags['StudyTime'] = str(ds.StudyTime)
    tags['StudyID'] = str(ds.StudyID)
    tags['Modality'] = str(ds.Modality)
    tags['StudyDescription'] = str(ds.StudyDescription)

    tags['SeriesDate'] = str(ds.SeriesDate)
    tags['SeriesTime'] = str(ds.SeriesTime)
    tags['SeriesDescription'] = str(ds.SeriesDescription)

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

    #print(meta_tags)

    # Simplify implement
    for v in meta_tags.splitlines()[1:]:
        group_element = v[:v.find(')')+1]
        tag_description = v[v.find(')')+2:v.find(':')-2]
        value = v[v.find(':')-2:]

        tag = list()
        tag.append({'(Group,Element)': group_element})
        tag.append({'(TAG Description)': tag_description})
        tag.append({'(Value)': value})
        tags.append(tag)



    # 안 씀
    # # tags[''] = str(ds.file_meta.)
    # tags['FileMetaInformationGroupLength'] = str(ds.file_meta.FileMetaInformationGroupLength)
    # tags['FileMetaInformationVersion'] = str(ds.file_meta.FileMetaInformationVersion)
    #
    # tags['MediaStorageSOPClassUID'] = str(ds.file_meta.MediaStorageSOPClassUID)
    # tags['MediaStorageSOPInstanceUID'] = str(ds.file_meta.MediaStorageSOPInstanceUID)
    #
    # tags['TransferSyntaxUID'] = str(ds.file_meta.TransferSyntaxUID)
    #
    # tags['ImplementationClassUID'] = str(ds.file_meta.ImplementationClassUID)
    # tags['ImplementationVersionName'] = str(ds.file_meta.ImplementationVersionName)
    #
    # tags['SourceApplicationEntityTitle'] = str(ds.file_meta.SourceApplicationEntityTitle)
    #
    # # tags[''] = str(ds.)
    # tags['ImageType'] = str(ds.ImageType)
    # tags['SOPClassUID'] = str(ds.SOPClassUID)
    # tags['SOPInstanceUID'] = str(ds.SOPInstanceUID)
    # tags['StudyDate'] = str(ds.StudyDate)
    # tags['SeriesDate'] = str(ds.SeriesDate)
    # tags['AcquisitionDate'] = str(ds.AcquisitionDate)
    # tags['ContentDate'] = str(ds.ContentDate)
    # tags['StudyTime'] = str(ds.StudyTime)
    # tags['SeriesTime'] = str(ds.SeriesTime)
    # tags['AcquisitionTime'] = str(ds.AcquisitionTime)
    # tags['ContentTime'] = str(ds.ContentTime)
    # tags['AccessionNumber'] = str(ds.AccessionNumber)
    # tags['Modality'] = str(ds.Modality)
    # tags['Manufacturer'] = str(ds.Manufacturer)
    # tags['InstitutionName'] = str(ds.InstitutionName)
    # tags['InstitutionAddress'] = str(ds.InstitutionAddress)
    # tags['ReferringPhysicianName'] = str(ds.ReferringPhysicianName)
    # tags['StationName'] = str(ds.StationName)
    # tags['StudyDescription'] = str(ds.StudyDescription)
    # tags['ProcedureCodeSequence'] = str(ds.ProcedureCodeSequence)
    #
    # tags['CodeValue'] = str(ds.ProcedureCodeSequence)
    #
    # # tags[''] = str(ds.)
    # # tags[''] = str(ds.)
    # # tags[''] = str(ds.)
    #
    # tags['PatientName'] = str(ds.PatientName)
    # tags['PatientID'] = str(ds.PatientID)
    # tags['PatientBirthDate'] = str(ds.PatientBirthDate)
    # tags['PatientSex'] = str(ds.PatientSex)
    # tags['PatientAge'] = str(ds.PatientAge)
    #
    # tags['StudyDate'] = str(ds.StudyDate)
    # tags['StudyTime'] = str(ds.StudyTime)
    # tags['StudyID'] = str(ds.StudyID)
    #
    # tags['StudyDescription'] = str(ds.StudyDescription)
    #
    # tags['SeriesDate'] = str(ds.SeriesDate)
    # tags['SeriesTime'] = str(ds.SeriesTime)
    # tags['SeriesDescription'] = str(ds.SeriesDescription)



    return tags