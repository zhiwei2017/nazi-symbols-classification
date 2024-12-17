import os
import shutil
from typing import Any, List

from fastapi import APIRouter, UploadFile, HTTPException
from ..schemas.classification import ClassifyResponse
from ..services.classification import get_classification_result

classification_router = APIRouter()

data_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                           "data")


@classification_router.post("/classify", response_model=ClassifyResponse)
async def classify(images: List[UploadFile]) -> Any:
    """Handles the classification of uploaded images, identifying specific symbols using a multi-layer model.

    This endpoint accepts multiple image files, saves them to a temporary directory, and processes
    them through a classification pipeline to detect specific symbols (e.g., "nazi-symbol"). The classification
    results include probabilities, detected symbols, and additional details.

    \f

    Args:
        images (List[UploadFile]): A list of uploaded image files to be classified.

    Returns:
        ClassifyResponse: A response model containing classification results for each image, including:
            - `containing_nazi_symbols`: Whether the image contains specific symbols.
            - `prob`: The confidence probability of the detected symbol.
            - `nazi_symbols`: List of identified symbols (if applicable).
            - `details`: Additional details about the detected symbols.

    Raises:
        HTTPException: If there is an error saving one or more uploaded images.

    Process:
        1. Images are saved to the `data_folder` directory.
        2. The `get_classification_result` function processes the images using the classification pipeline.
        3. Results are formatted and returned as a structured response.

    Example:
        >>> response = await classify([upload_file_1, upload_file_2])
        >>> print(response.results)
        [
            {
                "containing_nazi_symbols": True,
                "prob": 0.85,
                "nazi_symbols": ["swastika"],
                "details": [{"label": "swastika", "prob": 0.85}]
            },
            {
                "containing_nazi_symbols": False,
                "prob": 0.1,
                "nazi_symbols": [],
                "details": []
            }
        ]

    Notes:
        - The function uses a threshold of `0.1` for the second-layer model.
        - Images that fail to upload are reported in the response as an HTTPException.

    """
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
    if failed_images:
        message = (f"There was an error uploading the image{(len(failed_images) > 1) * 's'} "
                   f"[{', '.join(failed_images)}].")  # type: ignore
        return HTTPException(status_code=501, detail=message)

    classification_results = get_classification_result(image_paths, 0.1)
    results = []
    for classification_result in classification_results:
        containing_nazi_symbols = classification_result['first_layer_result']['label'] == "nazi-symbol"
        prob = classification_result['first_layer_result']['prob']
        nazi_symbols, details = [], []
        if containing_nazi_symbols:
            nazi_symbols = [d['label'] for d in classification_result['second_layer_result']]
            details = classification_result['second_layer_result']
        result = dict(containing_nazi_symbols=containing_nazi_symbols,
                      prob=prob,
                      nazi_symbols=nazi_symbols,
                      details=details)
        results.append(result)
    return ClassifyResponse(results=results)  # type: ignore
