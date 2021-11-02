from unittest import TestCase

from api.Service.dicom_viewer_service import convert_dicom_image_to_png

class Test(TestCase):
    def test_convert_dicom_image_to_png(self):


        convert_dicom_image_to_png(None)


        self.fail()
