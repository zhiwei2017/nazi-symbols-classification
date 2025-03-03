import cv2
import os
from nazi_symbols_classification.image_processing import (
    auto_resize, grayscale, auto_adjust_contrast
)
from nazi_symbols_classification.pipeline import Pipeline
from ultralytics import YOLO
from typing import List, Dict, Any
from ..globals import state

data_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                           "data")


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
    state["first_layer_model"] = YOLO(os.path.join(data_folder, "first-layer.pt"))
    state["second_layer_model"] = YOLO(os.path.join(data_folder, "second-layer.pt"))


def get_first_layer_result(images):
    # get first layer prediction result
    first_layer_names = state["first_layer_model"].names
    original_results = state["first_layer_model"](source=images, stream=True)
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
    original_results = state["second_layer_model"](source=images, stream=True)
    for i in range(len(results)):
        if results[i]["first_layer_result"]["label"] == "nazi-symbol":  # type: ignore
            original_result = original_results.pop(0)
            probs_result = original_result.probs
            top5_probs = probs_result.top5conf.numpy()
            probs = [prob for prob in top5_probs if prob >= second_layer_threshold]
            labels = [second_layer_names[label] for label in probs_result.top5[:len(probs)]]
            results[i]["second_layer_result"] = [dict(label=label, prob=prob)  # type: ignore
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
    state["image_preprocessing_pipeline"].run(image_paths)
    images = [cv2.imread(image_path) for image_path in image_paths]

    # get first layer prediction result
    results = get_first_layer_result(images)

    # Identify images requiring second-layer classification
    images_for_second_layer = []
    for i, image in enumerate(images):
        if results[i]["first_layer_result"]["label"] == "nazi-symbol":  # type: ignore
            images_for_second_layer.append(image)

    if images_for_second_layer:
        results = get_second_layer_result(images_for_second_layer, results, second_layer_threshold)

    return results
