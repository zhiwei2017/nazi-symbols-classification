import unittest
import os
import shutil
import tempfile
from nazi_symbols_classification.image_processing import (
    flip_image,
    randomly_flip_image, rotate_image, randomly_rotate_image, shear_image,
    randomly_shear_image, change_image_hue_saturation_brightness,
    randomly_change_image_hue_saturation_brightness,
    change_image_contrast_brightness, randomly_change_image_contrast_brightness,
    blur_image, randomly_blur_image, salt_pepper_noise, randomly_add_noise, FlipDirection,
    NonZeroSign
)


class TestImageProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup directories for test outputs
        cls.test_image_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
        cls.output_dir = tempfile.mkdtemp()

        # Use a simple image for testing
        cls.test_image = os.path.join(cls.test_image_dir, "test_image.jpg")
        assert os.path.exists(cls.test_image), "Test image not found!"

    @classmethod
    def tearDownClass(cls):
        # Cleanup generated output files
        shutil.rmtree(cls.output_dir)

    def test_flip_image(self):
        output = flip_image(self.test_image, FlipDirection.HORIZONTALLY, self.output_dir)
        self.assertTrue(os.path.exists(output))
        self.assertEqual(open(os.path.join(self.test_image_dir, "test_image_flipped_horizontally.jpg"), "rb").read(),
                         open(output, "rb").read())

        output = flip_image(self.test_image, FlipDirection.VERTICALLY, self.output_dir)
        self.assertTrue(os.path.exists(output))
        self.assertEqual(open(os.path.join(self.test_image_dir, "test_image_flipped_vertically.jpg"), "rb").read(),
                         open(output, "rb").read())

    def test_randomly_flip_image(self):
        directions = [FlipDirection.HORIZONTALLY, FlipDirection.VERTICALLY]
        output = randomly_flip_image(self.test_image, directions, self.output_dir)
        self.assertTrue(os.path.exists(output))

    def test_rotate_image(self):
        output = rotate_image(self.test_image, angle=45, output_folder=self.output_dir)
        self.assertTrue(os.path.exists(output))
        self.assertEqual(open(os.path.join(self.test_image_dir, "test_image_rotate_45.jpg"), "rb").read(),
                         open(output, "rb").read())

    def test_randomly_rotate_image(self):
        output = randomly_rotate_image(self.test_image, angle_range=90, output_folder=self.output_dir)
        self.assertTrue(os.path.exists(output))

    def test_shear_image(self):
        output = shear_image(self.test_image, 1, 20, 1, 15, self.output_dir)
        self.assertTrue(os.path.exists(output))
        self.assertEqual(open(os.path.join(self.test_image_dir, "test_image_shear_20_15.jpg"), "rb").read(),
                         open(output, "rb").read())

    def test_randomly_shear_image(self):
        output = randomly_shear_image(self.test_image, 20, 15, self.output_dir)
        self.assertTrue(os.path.exists(output))

    # def test_change_image_hue_saturation_brightness(self):
    #     output = change_image_hue_saturation_brightness(self.test_image, hue_change=30, output_folder=self.output_dir)
    #     self.assertTrue(os.path.exists(output))
    #     self.assertEqual(open(os.path.join(self.test_image_dir, "test_image_hue_30.jpg"), "rb").read(),
    #                      open(output, "rb").read())
    #
    #     output = change_image_hue_saturation_brightness(self.test_image, saturation_change=128, output_folder=self.output_dir)
    #     self.assertTrue(os.path.exists(output))
    #     self.assertEqual(open(os.path.join(self.test_image_dir, "test_image_saturation_128.jpg"), "rb").read(),
    #                      open(output, "rb").read())
    #
    #     output = change_image_hue_saturation_brightness(self.test_image, brightness_change=30,
    #                                                     output_folder=self.output_dir)
    #     self.assertTrue(os.path.exists(output))
    #     self.assertEqual(open(os.path.join(self.test_image_dir, "test_image_brightness_30.jpg"), "rb").read(),
    #                      open(output, "rb").read())
    #
    #     output = change_image_hue_saturation_brightness(self.test_image,
    #                                                     sign=NonZeroSign.NEG,
    #                                                     hue_change=30,
    #                                                     output_folder=self.output_dir)
    #     self.assertTrue(os.path.exists(output))
    #     self.assertEqual(open(os.path.join(self.test_image_dir, "test_image_hue_-30.jpg"), "rb").read(),
    #                      open(output, "rb").read())

    def test_randomly_change_image_hue_saturation_brightness(self):
        output = randomly_change_image_hue_saturation_brightness(self.test_image, hue_range=90, output_folder=self.output_dir)
        self.assertTrue(os.path.exists(output))

    def test_change_image_contrast_brightness(self):
        output = change_image_contrast_brightness(self.test_image,
                                                  contrast_control=1.5,
                                                  brightness_control=30,
                                                  output_folder=self.output_dir)
        self.assertTrue(os.path.exists(output))
        self.assertEqual(open(os.path.join(self.test_image_dir, "test_image_exposure_30.jpg"), "rb").read(),
                         open(output, "rb").read())

    def test_randomly_change_image_contrast_brightness(self):
        output = randomly_change_image_contrast_brightness(self.test_image,
                                                           contrast_control=1.5,
                                                           brightness_range_percentage=0.2,
                                                           output_folder=self.output_dir)
        self.assertTrue(os.path.exists(output))

    def test_blur_image(self):
        output = blur_image(self.test_image, output_folder=self.output_dir)
        self.assertTrue(os.path.exists(output))
        self.assertEqual(open(os.path.join(self.test_image_dir, "test_image_gaussian_blur.jpg"), "rb").read(),
                         open(output, "rb").read())

    def test_randomly_blur_image(self):
        output = randomly_blur_image(self.test_image, ksize_range=9, output_folder=self.output_dir)
        self.assertTrue(os.path.exists(output))

    def test_salt_pepper_noise(self):
        output = salt_pepper_noise(self.test_image, prob=0.05, output_folder=self.output_dir)
        self.assertTrue(os.path.exists(output))

    def test_randomly_add_noise(self):
        output = randomly_add_noise(self.test_image, prob_range=0.1, output_folder=self.output_dir)
        self.assertTrue(os.path.exists(output))
