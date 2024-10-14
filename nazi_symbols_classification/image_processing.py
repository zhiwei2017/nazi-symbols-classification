import cv2
import math
import numpy as np
import random
from typing import Tuple
from .constants import FlipDirection, NonZeroSign, ZeroSign
from .utils import get_image_name_extension


def auto_resize(path: str, new_width: int, new_height: int) -> None:
    """Automatically resize the image according to the given width and height.

    Args:
        path ():
        new_width ():
        new_height ():

    Returns:

    """
    # read image
    image = cv2.imread(path)

    # Get image dimensions
    height, width = image.shape[:2]
    width_ratio = new_width / width
    height_ratio = new_height / height
    if width_ratio == height_ratio:
        resized_image = cv2.resize(image, None, fx=width_ratio, fy=height_ratio)
    else:
        resized_image = cv2.resize(image, (new_width, new_height))
    cv2.imwrite(path, resized_image)


def grayscale(path: str) -> None:
    # Load the input image
    image = cv2.imread(path)

    # Use the cvtColor() function to grayscale the image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(path, gray_image)


def auto_adjust_contrast(path: str) -> None:
    image = cv2.imread(path, cv2.IMREAD_COLOR)

    # Convert the image from BGR to YCrCb color space
    ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

    # Split the image into Y, Cr, and Cb channels
    y_channel, cr_channel, cb_channel = cv2.split(ycrcb_image)

    # Perform contrast stretching on the Y channel
    y_channel_stretched = cv2.normalize(y_channel, None, 0, 255, cv2.NORM_MINMAX)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    y_channel_enhanced = clahe.apply(y_channel_stretched)

    # match algorithm:
    #     case "contrast_stretching":
    #         # Perform contrast stretching on the Y channel
    #         y_channel_enhanced = cv2.normalize(y_channel, None, 0, 255, cv2.NORM_MINMAX)
    #         clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    #         y_channel_enhanced = clahe.apply(y_channel_enhanced)
    #     case "histogram_equalization":
    #         # Perform histogram equalization on the stretched Y channel
    #         y_channel_enhanced = cv2.equalizeHist(y_channel)
    #     case "adaptive_equalization":
    #         clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    #         y_channel_enhanced = clahe.apply(y_channel)
    #     case _:
    #         raise ValueError("Unsupported Algorithm")

    # Merge the enhanced Y channel back with Cr and Cb channels
    enhanced_ycrcb_image = cv2.merge([y_channel_enhanced, cr_channel, cb_channel])

    # Convert the image back from YCrCb to BGR color space
    enhanced_image = cv2.cvtColor(enhanced_ycrcb_image, cv2.COLOR_YCrCb2BGR)
    cv2.imwrite(path, enhanced_image)


def flip_image(path: str, direction: FlipDirection) -> str:
    image_name, image_extension = get_image_name_extension(path)

    image = cv2.imread(path)
    flipped_image = cv2.flip(image, direction.value)

    output_path = f"{image_name}_flipped_{direction.name.lower()}.{image_extension}"
    cv2.imwrite(output_path, flipped_image)
    return output_path


def rotate_image(path: str, angle: float) -> str:
    """This function rotates a picture to given angle."""
    image_name, image_extension = get_image_name_extension(path)

    # Read the image
    image = cv2.imread(path)

    # Get image dimensions
    height, width = image.shape[:2]

    # Compute the center of the image
    center = (width / 2, height / 2)

    # Calculate rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1)

    # Apply the computed rotation matrix to the image
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    # Save the rotated image
    output_path = f"{image_name}_rotate_{angle}.{image_extension}"
    cv2.imwrite(output_path, rotated_image)
    return output_path


def randomly_rotate_image(path: str, angle_range: float) -> str:
    angle = random.uniform(-1 * angle_range, angle_range)
    return rotate_image(path, angle)


def shear_image(path: str,
                vertical_sign: NonZeroSign, vertical_angle: int,
                horizontal_sign: NonZeroSign, horizontal_angle: int):
    if vertical_angle < 0 or vertical_angle > 45:
        raise ValueError
    elif horizontal_angle < 0 or horizontal_angle > 45:
        raise ValueError
    image_name, image_extension = get_image_name_extension(path)
    # read the input image
    img = cv2.imread(path)
    # convert from BGR to RGB so we can plot using matplotlib
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # get the image shape
    rows, cols, dim = img.shape
    # transformation matrix for Shearing
    M = np.float32([[1, vertical_sign / math.tan(math.pi * (90 - vertical_angle) / 180), 0],
                    [horizontal_sign / math.tan(math.pi * (90 - horizontal_angle) / 180), 1, 0],
                    [0, 0, 1]])
    # apply a perspective transformation to the image
    sheared_img = cv2.warpPerspective(img, M, (int(cols), int(rows)))
    output_path = f"{image_name}_shear_{vertical_sign * vertical_angle}_{horizontal_sign * horizontal_angle}.{image_extension}"
    cv2.imwrite(output_path, sheared_img)
    return output_path


def randomly_shear_image(path: str,
                         vertical_angle_range: int,
                         horizontal_angle_range: int) -> str:
    if vertical_angle_range < 0 or vertical_angle_range > 45:
        raise ValueError
    elif horizontal_angle_range < 0 or horizontal_angle_range > 45:
        raise ValueError
    vertical_sign = random.choice(NonZeroSign.values())
    horizontal_sign = random.choice(NonZeroSign.values())
    vertical_angle = random.randint(0, vertical_angle_range)
    horizontal_angle = random.randint(0, horizontal_angle_range)
    return shear_image(path, vertical_sign, vertical_angle, horizontal_sign, horizontal_angle)


def change_image_hue_saturation_brightness(path: str,
                                           sign: NonZeroSign = 1,
                                           hue_change: int = 0,
                                           saturation_change: int = 0,
                                           brightness_change: int = 0) -> str:
    image_name, image_extension = get_image_name_extension(path)
    # read image
    img = cv2.imread(path)

    # convert img to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # shift the hue
    # cv2 will clip automatically to avoid color wrap-around
    file_name_suffix = ""
    if hue_change:
        h = cv2.add(h, sign * hue_change)
        file_name_suffix = f"hue_{sign * hue_change}"
    elif saturation_change:
        s = cv2.add(s, sign * saturation_change)
        file_name_suffix = f"saturation_{sign * saturation_change}"
    elif brightness_change:
        v = cv2.add(v, sign * brightness_change)
        file_name_suffix = f"brightness_{sign * brightness_change}"
    # combine new hue with s and v
    new_hsv = cv2.merge([h, s, v])

    # convert from HSV to BGR
    result = cv2.cvtColor(new_hsv, cv2.COLOR_HSV2BGR)

    output_path = f"{image_name}_{file_name_suffix}.{image_extension}"
    # save result
    cv2.imwrite(output_path, result)
    return output_path


def randomly_change_image_hue_saturation_brightness(path: str,
                                                    hue_range: int = 0,
                                                    saturation_range: float = 0,
                                                    brightness_range: float = 0) -> str:
    if hue_range < 0 or hue_range > 180:
        raise ValueError("Hue has to be in the interval [0, 180]")
    elif saturation_range < 0 or saturation_range > 1:
        raise ValueError("Saturation has to be in the interval [0, 1]")
    elif brightness_range < 0 or brightness_range > 1:
        raise ValueError("Brightness has to be in the interval [0, 1]")
    sign = random.choice(NonZeroSign.values())
    hue_change = random.randint(0, hue_range)
    saturation_change = random.randint(0, int(255 * saturation_range))
    brightness_change = random.randint(0, int(255 * saturation_range))
    return change_image_hue_saturation_brightness(path,
                                                  sign,
                                                  hue_change,
                                                  saturation_change,
                                                  brightness_change)


def change_image_contrast_brightness(path: str,
                                     sign: ZeroSign = 1,
                                     contrast_control: float = 1,
                                     brightness_control: int = 0) -> str:
    if brightness_control < 0 or brightness_control > 1:
        raise ValueError
    elif contrast_control < 0:
        raise ValueError
    image_name, image_extension = get_image_name_extension(path)
    img = cv2.imread(path)

    # define the contrast and brightness value
    # Contrast control, To lower the contrast, use 0 < alpha < 1. And for higher contrast use alpha > 1.
    # Brightness control, A good range for brightness value is [-127, 127]

    # call addWeighted function. use beta = 0 to effectively only operate on one image
    out = cv2.convertScaleAbs(img,
                              alpha=contrast_control,
                              beta=sign * brightness_control)
    output_path = f"{image_name}_brightness_{sign * brightness_control}.{image_extension}"
    cv2.imwrite(output_path, out)
    return output_path


def randomly_change_image_contrast_brightness(path: str,
                                              sign: ZeroSign = 0,
                                              contrast_control: float = 1,
                                              brightness_range_percentage: float = 0) -> str:
    if brightness_range_percentage < 0 or brightness_range_percentage > 1:
        raise ValueError
    brightness_range = int(brightness_range_percentage * 127)
    new_sign = sign or random.choice(ZeroSign.values())
    match sign:
        case ZeroSign.ZERO:
            brightness_control = random.randint(-1 * brightness_range, brightness_range)
        case ZeroSign.NEG:
            brightness_control = random.randint(-1 * brightness_range, 0)
        case ZeroSign.POS:
            brightness_control = random.randint(0, brightness_range)
        case _:
            raise ValueError("Unsupported value.")
    return change_image_contrast_brightness(path,
                                            new_sign,
                                            contrast_control,
                                            brightness_control)


def blur_image(path: str, ksize: Tuple[int, int] = (7, 7)) -> str:
    image_name, image_extension = get_image_name_extension(path)
    # Reading an image in default mode
    image = cv2.imread(path)

    # Using cv2.blur() method
    blurred_image = cv2.GaussianBlur(image, ksize, 0)

    output_path = f"{image_name}_gaussian_blur.{image_extension}"

    cv2.imwrite(output_path, blurred_image)
    return output_path


def salt_pepper_noise(path: str, prob: float) -> str:
    """
    Add salt and pepper noise to image
    prob: Probability of the noise
    """
    image_name, image_extension = get_image_name_extension(path)
    image = cv2.imread(path)
    output = image.copy()
    if len(image.shape) == 2:
        black = 0
        white = 255
    else:
        colorspace = image.shape[2]
        if colorspace == 3:  # RGB
            black = np.array([0, 0, 0], dtype='uint8')
            white = np.array([255, 255, 255], dtype='uint8')
        else:  # RGBA
            black = np.array([0, 0, 0, 255], dtype='uint8')
            white = np.array([255, 255, 255, 255], dtype='uint8')
    probs = np.random.random(output.shape[:2])
    output[probs < (prob / 2)] = black
    output[probs > 1 - (prob / 2)] = white

    output_path = f"{image_name}_noise_prob_{prob}.{image_extension}"
    cv2.imwrite(output_path, output)
    return output_path


def randomly_add_noise(path: str, prob_range: float) -> str:
    prob = random.uniform(0.0, prob_range)
    return salt_pepper_noise(path, prob)
