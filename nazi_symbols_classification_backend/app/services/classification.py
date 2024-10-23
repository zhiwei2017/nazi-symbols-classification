import cv2
import os
from nazi_symbols_classification.image_processing import (
    auto_resize, grayscale, auto_adjust_contrast
)
from nazi_symbols_classification.pipeline import Pipeline
from ultralytics import YOLO
from ..globals import state

data_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                           "data")


def init_state_for_classification():
    state["image_preprocessing_pipeline"] = Pipeline([
        ("auto_resize", auto_resize, dict(new_width=640, new_height=640)),
        ("grayscale", grayscale, None),
        ("auto_adjust_contrast", auto_adjust_contrast, None),
    ])
    state["first_layer_model"] = YOLO(os.path.join(data_folder, "first-layer.pt"))
    state["second_layer_model"] = YOLO(os.path.join(data_folder, "second-layer.pt"))


def get_classification_result(image_paths, second_layer_threshold=0.3):
    state["image_preprocessing_pipeline"].run(image_paths)
    images = [cv2.imread(image_path) for image_path in image_paths]

    # get first layer prediction result
    first_layer_names = state["first_layer_model"].names
    original_results = state["first_layer_model"].predict(images)
    results = []
    for original_result in original_results:
        probs_result = original_result.probs
        label = first_layer_names[probs_result.top1]
        prob = probs_result.top1conf.item()
        results.append(dict(first_layer_result=dict(label=label, prob=prob),
                            second_layer_result=list()))

    images_for_second_layer = []
    for i, image in enumerate(images):
        if results[i]["first_layer_result"]["label"] == "nazi-symbol":
            images_for_second_layer.append(image)

    if images_for_second_layer:
        second_layer_names = state["second_layer_model"].names
        original_results = state["second_layer_model"].predict(images_for_second_layer)
        for i in range(len(results)):
            if results[i]["first_layer_result"]["label"] == "nazi-symbol":
                original_result = original_results.pop(0)
                probs_result = original_result.probs
                top5_probs = probs_result.top5conf.numpy()
                probs = [prob for prob in top5_probs if prob >= second_layer_threshold]
                labels = [second_layer_names[label] for label in probs_result.top5[:len(probs)]]
                results[i]["second_layer_result"] = [dict(label=label, prob=prob) for label, prob in zip(labels, probs)]

    return results
