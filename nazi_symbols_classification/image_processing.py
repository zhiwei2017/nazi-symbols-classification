import os.path
import cv2
import math
import numpy as np
from random import SystemRandom
from typing import Tuple, Union, Optional
from .constants import FlipDirection, NonZeroSign, ZeroSign
from .utils import get_image_name_extension

crypto_gen = SystemRandom()


def auto_resize(path: str,
                new_width: int,
                new_height: int,
                output_folder: Optional[str] = None) -> str:
    """Automatically resizes an image to the specified dimensions.

    Args:
        path (str): Path to the input image file.
        new_width (int): Desired width of the resized image.
        new_height (int): Desired height of the resized image.
        output_folder (str, optional): folder for the output file. If None,
         modifies the image in place and saves it.

    Returns:
        str: The function modifies the image in place and saves it, if
        output_folder is not given. Otherwise, save the output file with same
        file name in output folder.
    """
    image = cv2.imread(path)
    height, width = image.shape[:2]
    width_ratio = new_width / width
    height_ratio = new_height / height
    if width_ratio == height_ratio:
        resized_image = cv2.resize(image, None, fx=width_ratio, fy=height_ratio)
    else:
        resized_image = cv2.resize(image, (new_width, new_height))
    output_path = path if not output_folder else os.path.join(output_folder,
                                                              os.path.basename(path))
    cv2.imwrite(output_path, resized_image)
    return output_path


def grayscale(path: str,
              output_folder: Optional[str] = None) -> str:
    """Converts an image to grayscale.

    Args:
        path (str): Path to the input image file.
        output_folder (str, optional): folder for the output file. If None,
         modifies the image in place and saves it.

    Returns:
        str: The function modifies the image in place and saves it, if
        output_folder is not given. Otherwise, save the output file with same
        file name in output folder.
    """
    image = cv2.imread(path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    output_path = path if not output_folder else os.path.join(output_folder,
                                                              os.path.basename(path))
    cv2.imwrite(output_path, gray_image)
    return output_path


def auto_adjust_contrast(path: str, output_folder: Optional[str] = None) -> str:
    """Enhances the contrast of an image using histogram equalization.

    Args:
        path (str): Path to the input image file.
        output_folder (str, optional): folder for the output file. If None,
         modifies the image in place and saves it.


    Returns:
        str: The function modifies the image in place and saves it, if
        output_folder is not given. Otherwise, save the output file with same
        file name in output folder.
    """
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y_channel, cr_channel, cb_channel = cv2.split(ycrcb_image)
    y_channel_stretched = cv2.normalize(y_channel, dst=None, alpha=0, beta=255,
                                        norm_type=cv2.NORM_MINMAX)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    y_channel_enhanced = clahe.apply(y_channel_stretched)
    enhanced_ycrcb_image = cv2.merge([y_channel_enhanced, cr_channel, cb_channel])
    enhanced_image = cv2.cvtColor(enhanced_ycrcb_image, cv2.COLOR_YCrCb2BGR)
    output_path = path if not output_folder else os.path.join(output_folder,
                                                              os.path.basename(path))
    cv2.imwrite(output_path, enhanced_image)
    return output_path


def flip_image(path: str,
               direction: FlipDirection,
               output_folder: Optional[str] = None) -> str:
    """Flips an image horizontally or vertically based on the specified direction.

    Args:
        path (str): Path to the input image file.
        direction (FlipDirection): Direction of the flip (horizontal or vertical).
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the flipped image.
    """
    input_folder_path, image_name, image_extension = get_image_name_extension(path)
    image = cv2.imread(path)
    flipped_image = cv2.flip(image, direction.value)
    output_folder_path = output_folder or input_folder_path
    image_name = os.path.join(output_folder_path, image_name)
    output_path = f"{image_name}_flipped_{direction.name.lower()}.{image_extension}"
    cv2.imwrite(output_path, flipped_image)
    return output_path


def randomly_flip_image(path: str,
                        directions: list[FlipDirection],
                        output_folder: Optional[str] = None) -> str:
    """Randomly flips an image based on the specified directions.

    Args:
        path (str): Path to the input image file.
        directions (list[FlipDirection]): List of possible flip directions.
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the flipped image.
    """
    direction = crypto_gen.choice(directions)
    return flip_image(path, direction, output_folder)


def rotate_image(path: str,
                 angle: float,
                 output_folder: Optional[str] = None) -> str:
    """Rotates an image by the specified angle.

    Args:
        path (str): Path to the input image file.
        angle (float): Rotation angle in degrees.
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the rotated image.
    """
    input_folder_path, image_name, image_extension = get_image_name_extension(path)
    image = cv2.imread(path)
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale=1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    output_folder_path = output_folder or input_folder_path
    image_name = os.path.join(output_folder_path, image_name)
    output_path = f"{image_name}_rotate_{angle}.{image_extension}"
    cv2.imwrite(output_path, rotated_image)
    return output_path


def randomly_rotate_image(path: str,
                          angle_range: float,
                          output_folder: Optional[str] = None) -> str:
    """Randomly rotates an image within the specified angle range.

    Args:
        path (str): Path to the input image file.
        angle_range (float): Maximum rotation angle range.
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the rotated image.
    """
    angle = crypto_gen.uniform(-1 * angle_range, angle_range)
    return rotate_image(path, angle, output_folder)


def shear_image(
    path: str,
    vertical_sign: NonZeroSign,
    vertical_angle: int,
    horizontal_sign: NonZeroSign,
    horizontal_angle: int,
    output_folder: Optional[str] = None
) -> str:
    """Applies vertical and horizontal shearing to an image.

    Args:
        path (str): Path to the input image file.
        vertical_sign (NonZeroSign): Direction for vertical shear.
        vertical_angle (int): Shear angle for the vertical direction (0-45 degrees).
        horizontal_sign (NonZeroSign): Direction for horizontal shear.
        horizontal_angle (int): Shear angle for the horizontal direction (0-45 degrees).
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the sheared image.

    Raises:
        ValueError: If the angles are outside the range of 0-45 degrees.
    """
    if vertical_angle < 0 or vertical_angle > 45:
        raise ValueError("Vertical angle must be between 0 and 45 degrees.")
    elif horizontal_angle < 0 or horizontal_angle > 45:
        raise ValueError("Horizontal angle must be between 0 and 45 degrees.")
    input_folder_path, image_name, image_extension = get_image_name_extension(path)
    img = cv2.imread(path)
    rows, cols, _ = img.shape
    M = np.float32([
        [1, vertical_sign / math.tan(math.pi * (90 - vertical_angle) / 180), 0],
        [horizontal_sign / math.tan(math.pi * (90 - horizontal_angle) / 180), 1, 0],
        [0, 0, 1],
    ])
    sheared_img = cv2.warpPerspective(img, M, (int(cols), int(rows)))
    output_folder_path = output_folder or input_folder_path
    image_name = os.path.join(output_folder_path, image_name)
    output_path = (f"{image_name}_shear_{vertical_sign * vertical_angle}_"
                   f"{horizontal_sign * horizontal_angle}.{image_extension}")
    cv2.imwrite(output_path, sheared_img)
    return output_path


def randomly_shear_image(
    path: str,
    vertical_angle_range: int,
    horizontal_angle_range: int,
    output_folder: Optional[str] = None
) -> str:
    """Applies random vertical and horizontal shearing to an image.

    Args:
        path (str): Path to the input image file.
        vertical_angle_range (int): Maximum vertical shear angle (0-45 degrees).
        horizontal_angle_range (int): Maximum horizontal shear angle (0-45 degrees).
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the sheared image.

    Raises:
        ValueError: If angle ranges are outside the valid range of 0-45 degrees.
    """
    if vertical_angle_range < 0 or vertical_angle_range > 45:
        raise ValueError("Vertical angle range must be between 0 and 45 degrees.")
    elif horizontal_angle_range < 0 or horizontal_angle_range > 45:
        raise ValueError("Horizontal angle range must be between 0 and 45 degrees.")
    vertical_sign = crypto_gen.choice(NonZeroSign.values())
    horizontal_sign = crypto_gen.choice(NonZeroSign.values())
    vertical_angle = crypto_gen.randint(0, vertical_angle_range)
    horizontal_angle = crypto_gen.randint(0, horizontal_angle_range)
    return shear_image(path, vertical_sign, vertical_angle, horizontal_sign,
                       horizontal_angle, output_folder)


def change_image_hue_saturation_brightness(
    path: str,
    sign: NonZeroSign = NonZeroSign.POS,
    hue_change: int = 0,
    saturation_change: int = 0,
    brightness_change: int = 0,
    output_folder: Optional[str] = None
) -> str:
    """Adjusts the hue, saturation, or brightness of an image.

    Args:
        path (str): Path to the input image file.
        sign (NonZeroSign): Sign to indicate the direction of adjustment.
        hue_change (int): Amount of hue adjustment (0-180).
        saturation_change (int): Amount of saturation adjustment.
        brightness_change (int): Amount of brightness adjustment.
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the modified image.
    """
    input_folder_path, image_name, image_extension = get_image_name_extension(path)
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    file_name_suffix = ""

    if hue_change:
        h = cv2.add(h, sign * hue_change)  # Adjust hue
        file_name_suffix = f"hue_{sign * hue_change}"
    elif saturation_change:
        s = cv2.add(s, sign * saturation_change)  # Adjust saturation
        file_name_suffix = f"saturation_{sign * saturation_change}"
    elif brightness_change:
        v = cv2.add(v, sign * brightness_change)  # Adjust brightness
        file_name_suffix = f"brightness_{sign * brightness_change}"

    new_hsv = cv2.merge([h, s, v])
    result = cv2.cvtColor(new_hsv, cv2.COLOR_HSV2BGR)
    output_folder_path = output_folder or input_folder_path
    image_name = os.path.join(output_folder_path, image_name)
    output_path = f"{image_name}_{file_name_suffix}.{image_extension}"
    cv2.imwrite(output_path, result)
    return output_path


def randomly_change_image_hue_saturation_brightness(
    path: str,
    hue_range: int = 0,
    saturation_range: float = 0.0,
    brightness_range: float = 0.0,
    output_folder: Optional[str] = None
) -> str:
    """Randomly adjusts the hue, saturation, and brightness of an image.

    Args:
        path (str): Path to the input image file.
        hue_range (int): Maximum hue adjustment range (0-180).
        saturation_range (float): Maximum saturation adjustment range (0-1).
        brightness_range (float): Maximum brightness adjustment range (0-1).
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the modified image.

    Raises:
        ValueError: If any parameter is out of its valid range.
    """
    if hue_range < 0 or hue_range > 180:
        raise ValueError("Hue range must be between 0 and 180.")
    elif saturation_range < 0 or saturation_range > 1:
        raise ValueError("Saturation range must be between 0 and 1.")
    elif brightness_range < 0 or brightness_range > 1:
        raise ValueError("Brightness range must be between 0 and 1.")
    sign = crypto_gen.choice(NonZeroSign.values())
    hue_change = crypto_gen.randint(0, hue_range)
    saturation_change = crypto_gen.randint(0, int(255 * saturation_range))
    brightness_change = crypto_gen.randint(0, int(255 * brightness_range))
    return change_image_hue_saturation_brightness(
        path, sign, hue_change, saturation_change, brightness_change, output_folder
    )


def change_image_contrast_brightness(
    path: str,
    sign: ZeroSign = ZeroSign.POS,
    contrast_control: float = 1.0,
    brightness_control: int = 0,
    output_folder: Optional[str] = None
) -> str:
    """Adjusts the contrast and brightness of an image.

    Args:
        path (str): Path to the input image file.
        sign (ZeroSign): Indicates the direction of brightness adjustment.
        contrast_control (float): Factor to control contrast (≥ 0).
        brightness_control (int): Value to adjust brightness (-127 to 127).
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the modified image.

    Raises:
        ValueError: If contrast_control is negative or brightness_control is out of range.
    """
    if abs(brightness_control) > 127:
        raise ValueError("Brightness control must be in the range [-127, 127].")
    elif contrast_control < 0:
        raise ValueError("Contrast control must be non-negative.")
    input_folder_path, image_name, image_extension = get_image_name_extension(path)
    img = cv2.imread(path)
    out = cv2.convertScaleAbs(img, alpha=contrast_control, beta=sign * brightness_control)
    output_folder_path = output_folder or input_folder_path
    image_name = os.path.join(output_folder_path, image_name)
    output_path = f"{image_name}_exposure_{sign * brightness_control}.{image_extension}"
    cv2.imwrite(output_path, out)
    return output_path


def randomly_change_image_contrast_brightness(
    path: str,
    sign: ZeroSign = ZeroSign.ZERO,
    contrast_control: float = 1.0,
    brightness_range_percentage: float = 0.0,
    output_folder: Optional[str] = None
) -> str:
    """Randomly adjusts the contrast and brightness of an image.

    Args:
        path (str): Path to the input image file.
        sign (ZeroSign): Indicates the direction of brightness adjustment.
        contrast_control (float): Factor to control contrast (≥ 0).
        brightness_range_percentage (float): Maximum brightness adjustment percentage (0-1).
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the modified image.

    Raises:
        ValueError: If brightness_range_percentage is outside [0, 1].
    """
    if brightness_range_percentage < 0 or brightness_range_percentage > 1:
        raise ValueError("Brightness range percentage must be between 0 and 1.")
    brightness_range = int(brightness_range_percentage * 127)
    match sign:
        case ZeroSign.ZERO:
            brightness_control = crypto_gen.randint(-1 * brightness_range,
                                                    brightness_range)
        case ZeroSign.NEG:
            brightness_control = crypto_gen.randint(-1 * brightness_range, 0)
        case ZeroSign.POS:
            brightness_control = crypto_gen.randint(0, brightness_range)
        case _:
            raise ValueError("Unsupported value.")
    return change_image_contrast_brightness(path, ZeroSign.POS, contrast_control,
                                            brightness_control, output_folder)


def blur_image(path: str,
               ksize: Tuple[int, int] = (7, 7),
               output_folder: Optional[str] = None) -> str:
    """Applies Gaussian blur to an image.

    Args:
        path (str): Path to the input image file.
        ksize (Tuple[int, int]): Kernel size for the Gaussian blur.
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the blurred image.
    """
    input_folder_path, image_name, image_extension = get_image_name_extension(path)
    image = cv2.imread(path)
    blurred_image = cv2.GaussianBlur(image, ksize, 0)
    output_folder_path = output_folder or input_folder_path
    image_name = os.path.join(output_folder_path, image_name)
    output_path = f"{image_name}_gaussian_blur.{image_extension}"
    cv2.imwrite(output_path, blurred_image)
    return output_path


def randomly_blur_image(path: str,
                        ksize_range: int = 7,
                        output_folder: Optional[str] = None) -> str:
    """Randomly applies Gaussian blur to an image.

    Args:
        path (str): Path to the input image file.
        ksize_range (int): Maximum kernel size range for the Gaussian blur.
        output_folder (str, optional): folder for the output file. If None,
         modifies the image in place and saves it.

    Returns:
        str: Path to the blurred image.
    """
    ksize = crypto_gen.randrange(1, ksize_range + 1, 2)
    return blur_image(path, ksize=(ksize, ksize), output_folder=output_folder)


def salt_pepper_noise(path: str,
                      prob: float,
                      output_folder: Optional[str] = None) -> str:
    """Adds salt-and-pepper noise to an image.

    Args:
        path (str): Path to the input image file.
        prob (float): Probability of noise in the range [0, 1].
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the noisy image.
    """
    input_folder_path, image_name, image_extension = get_image_name_extension(path)
    image = cv2.imread(path)
    output = image.copy()
    if len(image.shape) == 2:
        black: Union[int, np.ndarray] = 0
        white: Union[int, np.ndarray] = 255
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
    output_folder_path = output_folder or input_folder_path
    image_name = os.path.join(output_folder_path, image_name)
    output_path = f"{image_name}_noise_prob_{prob}.{image_extension}"
    cv2.imwrite(output_path, output)
    return output_path


def randomly_add_noise(path: str,
                       prob_range: float,
                       output_folder: Optional[str] = None) -> str:
    """Randomly adds salt-and-pepper noise to an image.

    Args:
        path (str): Path to the input image file.
        prob_range (float): Maximum probability of noise in the range [0, 1].
        output_folder (str, optional): folder for the output file. If None,
         the modified file will be saved in the same folder as the input image.

    Returns:
        str: Path to the noisy image.
    """
    prob = crypto_gen.uniform(0.0, prob_range)
    return salt_pepper_noise(path, prob, output_folder)
