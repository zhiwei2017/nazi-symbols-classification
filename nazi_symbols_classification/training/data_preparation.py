import os
import shutil
from roboflow import Roboflow


def download_data_from_roboflow(api_key, version, dataset_name,
                                dataset_parent_path="./datasets"):
    dataset_path = f"{dataset_parent_path}/{dataset_name}"
    rf = Roboflow(api_key=api_key)
    project = rf.workspace("zhiwei").project(dataset_name)
    version = project.version(version)
    version.download("folder", dataset_path)


def reorganise_images(path="./datasets/nazi-symbols-classification",
                      sub_folders=("train", "test", "valid")):
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


def remap_images(class_map,
                 path="./datasets/nazi-symbols-classification",
                 sub_folders=("train", "test", "valid")):
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


def get_paths_in_dir(dir_path):
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


def get_image_paths(path="./datasets/nazi-symbols-classification",
                    sub_folders=("train", "test", "val")):
    image_paths = []
    if sub_folders:
        for sub_folder_name in sub_folders:
            sub_folder_path = os.path.join(path, sub_folder_name)
            image_paths += get_paths_in_dir(sub_folder_path)
    else:
        image_paths += get_paths_in_dir(path)
    return image_paths
