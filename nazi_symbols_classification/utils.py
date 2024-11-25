import os
from typing import Tuple


def get_image_name_extension(image_path: str) -> Tuple[str, str, str]:
    """
    Extracts the folder path, image name, and image extension from the given image path.

    Args:
        image_path (str): The full file path to the image.

    Returns:
        Tuple[str, str, str]: A tuple containing:
            - folder_path (str): The directory where the image is located.
            - image_name (str): The name of the image file (without extension).
            - image_extension (str): The file extension of the image.

    Example:
        >>> folder, name, extension = get_image_name_extension("images/sample_image.jpg")
        >>> folder
        'images'
        >>> name
        'sample_image'
        >>> extension
        'jpg'
    """
    image_full_name = os.path.basename(image_path)
    folder_path = os.path.dirname(image_path)
    image_extension = image_full_name.split('.')[-1]
    image_name = image_full_name.removesuffix(f".{image_extension}")
    return folder_path, image_name, image_extension
