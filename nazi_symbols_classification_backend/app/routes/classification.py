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
    print(data_folder)
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
    return ClassifyResponse(results=results)
