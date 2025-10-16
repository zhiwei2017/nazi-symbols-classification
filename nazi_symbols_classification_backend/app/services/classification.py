import cv2
from PIL import Image
import os
import open_clip
import torch
import joblib
import numpy as np
from sklearn.svm import SVC
from nazi_symbols_classification.image_processing import (
    auto_resize, grayscale, auto_adjust_contrast
)
from nazi_symbols_classification.pipeline import Pipeline
from ultralytics import YOLO
from typing import List, Dict, Any
from ..globals import state
from ..configs import get_settings
from ..constants import AvailableEndpoints

setting = get_settings()
data_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                           "data")


class OpenCLIPTransformerSVC:
    def __init__(self, svc_model_path: str,
                 openclip_model_name: str = 'ViT-B-32',
                 device: str = "cpu"):
        self.openclip_model, _, self.preprocess = open_clip.create_model_and_transforms(
            openclip_model_name, pretrained="laion2b_s34b_b79k", device=device
        )
        self.openclip_model.eval()
        self.device = device
        self.model = joblib.load(svc_model_path)

    def encode_image(self, image):
        """Encodes an image into a feature vector using OpenCLIP."""
        with torch.no_grad(), torch.autocast(self.device):
            image = self.preprocess(image).unsqueeze(0)
            image = image.to(self.device)
            image_features = self.openclip_model.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)
            return image_features.cpu().float().numpy()

    def predict(self, image):
        """Predicts the class of an image using the SVC model."""
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        elif isinstance(image, Image.Image):
            image = image.convert("RGB")
        elif isinstance(image, np.ndarray):
            image = Image.fromarray(image).convert("RGB")
        image_features = self.encode_image(image)
        prediction = self.model.predict(image_features)
        return prediction[0]


def init_state_for_classification():
    """Initializes the global `state` dictionary with configurations required for image classification.

    This function sets up:
    - An image preprocessing pipeline with resizing, grayscale conversion, and contrast adjustment steps.
    - The first-layer YOLO model for initial classification.
    - The second-layer YOLO model for refined classification.

    The models are loaded from predefined paths in the `data_folder`, and the preprocessing pipeline
    includes the following steps:
        1. `auto_resize`: Resizes images to 640x640.
        2. `grayscale`: Converts images to grayscale.
        3. `auto_adjust_contrast`: Adjusts the contrast of the images.

    Global State Updates:
        state["image_preprocessing_pipeline"]: Pipeline object for preprocessing images.
        state["first_layer_model"]: YOLO model object for the first layer of classification.
        state["second_layer_model"]: YOLO model object for the second layer of classification.

    Raises:
        KeyError: If the global `state` dictionary is not defined.
        FileNotFoundError: If the model files are not found at the specified paths.

    Example:
        >>> init_state_for_classification()
        >>> print(state["image_preprocessing_pipeline"])
        Pipeline([...])
        >>> print(state["first_layer_model"])
        <YOLO model object>
    """
    state["image_preprocessing_pipeline"] = Pipeline([
        ("auto_resize", auto_resize, dict(new_width=640, new_height=640)),
        ("grayscale", grayscale, None),
        ("auto_adjust_contrast", auto_adjust_contrast, None),
    ])
    if (setting.AVAILABLE_ENDPOINTS in {AvailableEndpoints.BINARY,
                                        AvailableEndpoints.COMBINED,
                                        AvailableEndpoints.ALL}):
        if setting.FIRST_LAYER_MODEL == "SVC":
            state["first_layer_model"] = OpenCLIPTransformerSVC(
                svc_model_path=os.path.join(data_folder, "first-layer.pt"),
                openclip_model_name="ViT-B-32",
                device="cuda" if torch.cuda.is_available() else "cpu"
            )
        elif setting.FIRST_LAYER_MODEL == "YOLO":
            state["first_layer_model"] = YOLO(os.path.join(data_folder, "first-layer.pt"))
        else:
            raise ValueError(f"Unsupported first layer model: {setting.FIRST_LAYER_MODEL}")
    if (setting.AVAILABLE_ENDPOINTS in {AvailableEndpoints.MULTICLASS,
                                        AvailableEndpoints.COMBINED,
                                        AvailableEndpoints.ALL}):
        state["second_layer_model"] = YOLO(os.path.join(data_folder, "second-layer.pt"))
        if torch.cuda.is_available():
            state["second_layer_model"] = state["second_layer_model"].to("cuda")


def preprocess_images(image_paths: List[str]) -> None:
    """Preprocesses a list of images using the global image preprocessing pipeline.

    This function modifies the images in place by applying a series of preprocessing steps
    defined in the global `state["image_preprocessing_pipeline"]`. The preprocessing steps
    typically include resizing, converting to grayscale, and adjusting contrast.

    Args:
        image_paths (List[str]): A list of paths to the images to preprocess.

    Raises:
        KeyError: If the global `state` dictionary does not contain the required preprocessing pipeline.
        FileNotFoundError: If any of the image files are not found at the specified paths.

    Example:
        >>> preprocess_images(["path/to/image1.jpg", "path/to/image2.jpg"])
        >>> # The images at the specified paths are now preprocessed.
    """
    if "image_preprocessing_pipeline" not in state:
        raise KeyError("Image preprocessing pipeline is not initialized in the global state.")
    state["image_preprocessing_pipeline"].run(image_paths)


def get_first_layer_result(images):
    if setting.FIRST_LAYER_MODEL == "SVC":
    # get first layer prediction result
        return get_svc_first_layer_result(images)
    elif setting.FIRST_LAYER_MODEL == "YOLO":
        # get first layer prediction result
        return get_yolo_first_layer_result(images)
    else:
        raise ValueError(f"Unsupported first layer model: {setting.FIRST_LAYER_MODEL}")


def get_svc_first_layer_result(images):
    # get first layer prediction result
    result = []
    for image in images:
        predicted_label = state["first_layer_model"].predict(image)
        result.append(dict(first_layer_result=dict(label=predicted_label,
                                                    prob=None),
                           second_layer_result=list()))
    return result


def get_yolo_first_layer_result(images):
    # get first layer prediction result
    first_layer_names = state["first_layer_model"].names
    original_results = state["first_layer_model"](source=images, stream=False)
    results = []
    for original_result in original_results:
        probs_result = original_result.probs
        label = first_layer_names[probs_result.top1]
        prob = probs_result.top1conf.item()
        results.append(dict(first_layer_result=dict(label=label, prob=prob),
                            second_layer_result=list()))
    return results


def get_second_layer_result(images, results, second_layer_threshold: float = 0.3):
    second_layer_names = state["second_layer_model"].names
    original_results = state["second_layer_model"](source=images, stream=False)
    for i in range(len(results)):
        if results[i]["first_layer_result"]["label"] == "nazi-symbol":  # type: ignore
            original_result = original_results.pop(0)
            probs_result = original_result.probs
            top5_probs = probs_result.top5conf.numpy()
            probs = [prob for prob in top5_probs if prob >= second_layer_threshold]
            labels = [second_layer_names[label] for label in probs_result.top5[:len(probs)]]
            results[i]["second_layer_result"] = [dict(label=setting.CLASSIFICATION_LABEL_TRANSLATIONS[label], prob=prob)  # type: ignore
                                                 for label, prob in zip(labels, probs)]
    return results


def get_classification_result(image_paths: List[str],
                              second_layer_threshold: float = 0.3) -> List[Dict[str, Any]]:
    """Processes a list of image paths to classify them using a two-layer classification model.

    The function first preprocesses the images using a preprocessing pipeline, performs predictions
    using the first layer model, and identifies images requiring further classification. For these images,
    predictions are refined using a second-layer model with a specified confidence threshold.

    Args:
        image_paths (List[str]): A list of paths to the images to classify.
        second_layer_threshold (float): Confidence threshold for second-layer predictions.
            Only predictions with confidence >= `second_layer_threshold` are considered. Default is 0.3.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing classification results. Each dictionary includes:
            - "first_layer_result": A dictionary with:
                - "label" (str): Predicted label from the first-layer model.
                - "prob" (float): Confidence of the prediction from the first-layer model.
            - "second_layer_result": A list of dictionaries, each containing:
                - "label" (str): Predicted label from the second-layer model.
                - "prob" (float): Confidence of the prediction from the second-layer model.

    Raises:
        KeyError: If the required models or preprocessing pipelines are not available in the `state` dictionary.

    Example:
        >>> results = get_classification_result(["path/to/image1.jpg", "path/to/image2.jpg"])
        >>> print(results)
        [
            {
                "first_layer_result": {"label": "object-label", "prob": 0.95},
                "second_layer_result": [
                    {"label": "sub-label-1", "prob": 0.85},
                    {"label": "sub-label-2", "prob": 0.7}
                ]
            }
        ]
    """
    # get first layer prediction result
    results = get_first_layer_result(image_paths)

    # Identify images requiring second-layer classification
    images_for_second_layer = []
    for i, image in enumerate(image_paths):
        if results[i]["first_layer_result"]["label"] == "nazi-symbol":  # type: ignore
            images_for_second_layer.append(image)

    if images_for_second_layer:
        results = get_second_layer_result(images_for_second_layer, results, second_layer_threshold)

    return results
