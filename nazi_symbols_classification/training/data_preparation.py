import os
import shutil
import pandas as pd

from loguru import logger
from roboflow import Roboflow
from typing import Sequence, Dict, List


def download_data_from_roboflow(api_key: str,
                                version: str,
                                dataset_name: str,
                                dataset_parent_path: str = "./datasets"):
    """Downloads a dataset from Roboflow and saves it to the specified path.

    Args:
        api_key (str): Your Roboflow API key.
        version (str): The version of the dataset to download.
        dataset_name (str): The name of the dataset to download.
        dataset_parent_path (str): The parent directory where the dataset will be saved.

    Returns:
        None
    """
    dataset_path = f"{dataset_parent_path}/{dataset_name}"
    rf = Roboflow(api_key=api_key)
    project = rf.workspace("zhiwei").project(dataset_name)
    project_version = project.version(version)
    project_version.download("folder", dataset_path)


def reorganise_images(path: str = "./datasets/nazi-symbols-classification",
                      sub_folders: Sequence[str] = ("train", "test", "valid")):
    """Reorganises images in the specified path by splitting directories with multiple classes into separate directories.

    Args:
        path (str): The path to the dataset directory.
        sub_folders (Sequence[str]): A sequence of sub-folder names to process within the dataset directory.

    Returns:
        None
    """
    for sub_folder_name in sub_folders:
        sub_folder_path = os.path.join(path, sub_folder_name)
        for dir_name in os.listdir(sub_folder_path):
            if dir_name.startswith("."):
                continue
            elif " " in dir_name:
                classes = dir_name.split(" ")
                dir_path = os.path.join(sub_folder_path, dir_name)
                for class_dir in classes:
                    shutil.copytree(dir_path, os.path.join(sub_folder_path, class_dir), dirs_exist_ok=True)
                shutil.rmtree(dir_path)


def remap_images(class_map: Dict[str, Sequence[str]],
                 path: str = "./datasets/nazi-symbols-classification",
                 sub_folders: Sequence[str] = ("train", "test", "valid")):
    """Remaps images in the specified path according to the provided class mapping.

    Args:
        class_map (Dict[str, Sequence[str]]): A dictionary mapping target class names to lists of source class names.
        path (str): The path to the dataset directory.
        sub_folders (Sequence[str]): A sequence of sub-folder names to process within the dataset directory.

    Returns:

    """
    for sub_folder_name in sub_folders:
        sub_folder_path = os.path.join(path, sub_folder_name)
        for target, cls_list in class_map.items():
            target_path = os.path.join(sub_folder_path, target)
            if not cls_list:
                shutil.rmtree(target_path)
                continue
            elif not os.path.exists(target_path):
                os.mkdir(target_path)

            for cls in cls_list:
                source_path = os.path.join(sub_folder_path, cls)
                if cls == target:
                    continue
                elif not os.path.exists(source_path):
                    continue
                shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                shutil.rmtree(source_path)


def get_paths_in_dir(dir_path: str) -> Sequence[str]:
    """Retrieves all file paths in the specified directory and its sub-directories.

    Args:
        dir_path (str): The path to the directory from which to retrieve file paths.

    Returns:
        Sequence[str]: A list of file paths found in the specified directory and its sub-directories.
    """
    paths = []
    for name in os.listdir(dir_path):
        sub_dir_path = os.path.join(dir_path, name)
        if name.startswith("."):
            continue
        elif not os.path.isdir(sub_dir_path):
            continue
        paths += [os.path.join(sub_dir_path, file_name)
                  for file_name in os.listdir(sub_dir_path)
                  if not file_name.startswith(".")]
    return paths


def get_image_paths(path: str = "./datasets/nazi-symbols-classification",
                    sub_folders: Sequence[str] = ("train", "test", "val")) -> Sequence[str]:
    """Retrieves image paths from the specified directory and its sub-folders.

    Args:
        path (str): The path to the dataset directory.
        sub_folders (Sequence[str]): A sequence of sub-folder names to search for images. If empty, searches the main directory.

    Returns:
        Sequence[str]: A list of image paths found in the specified directory and its sub-folders.
    """
    image_paths: List[str] = []
    if sub_folders:
        for sub_folder_name in sub_folders:
            sub_folder_path = os.path.join(path, sub_folder_name)
            image_paths += get_paths_in_dir(sub_folder_path)
    else:
        image_paths += get_paths_in_dir(path)
    return image_paths


def load_labels_df(dataset_path: str,
                   sub_dataset_name: str = "train",
                   binary: bool = True) -> pd.DataFrame:
    """Loads labels from the specified dataset path and sub-dataset name.

    Args:
        dataset_path (str): The path to the dataset directory.
        sub_dataset_name (str): The name of the sub-dataset to load labels from (default is "train").
        binary (bool): if the data is loaded for binary classification (default is True).

    Returns:
        pd.DataFrame: A DataFrame containing the image paths and their corresponding labels.
    """
    image_paths = get_image_paths(dataset_path, sub_folders=(sub_dataset_name,))
    logger.info(f"Number of images in {sub_dataset_name} is {len(image_paths)}")
    training_image_paths = [image.removeprefix(f"os.path.join(dataset_path, sub_dataset_name)/") for image in image_paths]
    if binary:
        training_labels: List[int] = [int('non-nazi' not in image) for image in training_image_paths]
        labels = pd.DataFrame(dict(path=training_image_paths, contained_nazi=training_labels))
    else:
        training_labels: List[str] = [os.path.basename(os.path.dirname(image)) for image in training_image_paths]  # type: ignore
        labels = pd.DataFrame(dict(path=training_image_paths, nazi_cls=training_labels))
    return labels
