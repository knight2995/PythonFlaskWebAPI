from unittest import TestCase

import pydicom

from app.api.service.dicom_viewer_service import get_tags_all

class Test(TestCase):
    def test_dicom_data_view(self):


        ds: pydicom.FileDataset = pydicom.read_file('10007.dcm')

        get_tags_all(ds)




