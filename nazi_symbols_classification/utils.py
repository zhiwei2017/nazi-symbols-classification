from typing import Tuple


def get_image_name_extension(image_path: str) -> Tuple[str, str]:
    image_extension = image_path.split('.')[-1]
    image_name = image_path.removesuffix(f".{image_extension}")
    return image_name, image_extension
