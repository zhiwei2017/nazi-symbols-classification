import os
import shutil
from typing import Tuple, List
from fastapi import APIRouter, UploadFile, HTTPException


def save_images_to_folder(images: List[UploadFile],
                          data_folder: str) -> Tuple[List[str], List[str | None]]:
    """Save uploaded images to a specified folder.

    Args:
        images (): List of uploaded image files.
        data_folder (str): Folder where images will be saved.

    Returns:
        Tuple containing a list of failed image filenames and a list of saved image paths.
    """
    """
    

    :param images: 
    :param data_folder: 
    :return: 
    """
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    failed_images = []
    image_paths = []
    for image in images:
        try:
            image_path = os.path.join(data_folder, image.filename)  # type: ignore
            with open(image_path, 'wb') as f:
                shutil.copyfileobj(image.file, f)
            image_paths.append(image_path)
        except Exception:
            failed_images.append(image.filename)
        finally:
            image.file.close()
    return image_paths, failed_images
