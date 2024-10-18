import os
import shutil
from typing import Any, List
from fastapi import APIRouter, UploadFile, HTTPException
from ..schemas.classification import ClassifyResponse
from ..globals import state

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
    print(image_paths)
    state["image_preprocessing_pipeline"].run(image_paths)
    return ClassifyResponse(nazi_symbol="swastika", prob=0.9, details=[])
