from .image_processing import (
    auto_resize, grayscale, auto_adjust_contrast,
    randomly_flip_image, randomly_rotate_image, randomly_shear_image,
    randomly_change_image_hue_saturation_brightness,
    randomly_change_image_contrast_brightness, randomly_blur_image,
    randomly_add_noise
)
from .constants import FlipDirection
from .pipeline import Pipeline

preprocessing_pipeline = Pipeline([
    ("auto_resize", auto_resize, dict(new_width=640, new_height=640)),
    ("grayscale", grayscale, None),
    ("auto_adjust_contrast", auto_adjust_contrast, None),
])

augmentation_pipeline = Pipeline([
    ("randomly_flip_image", randomly_flip_image,
     dict(directions=(FlipDirection.HORIZONTALLY, FlipDirection.VERTICALLY))),
    ("randomly_rotate_image", randomly_rotate_image, dict(angle_range=15)),
    ("randomly_shear_image", randomly_shear_image,
     dict(vertical_angle_range=10, horizontal_angle_range=10)),
    ("randomly_change_image_hue", randomly_change_image_hue_saturation_brightness,
     dict(hue_range=15, saturation_range=0, brightness_range=0)),
    ("randomly_change_image_saturation",
     randomly_change_image_hue_saturation_brightness,
     dict(hue_range=0, saturation_range=0.25, brightness_range=0)),
    ("randomly_change_image_brightness",
     randomly_change_image_hue_saturation_brightness,
     dict(hue_range=0, saturation_range=0, brightness_range=0.15)),
    ("randomly_change_image_exposure",
     randomly_change_image_contrast_brightness,
     dict(sign=0, contrast_control=1, brightness_range_percentage=0.1)),
    ("randomly_blur_image", randomly_blur_image, dict(ksize_range=7)),
    ("randomly_add_noise", randomly_add_noise, dict(prob_range=0.001)),
])
