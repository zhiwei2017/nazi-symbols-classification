# how to train the model with existing datasets

## Download datasets
Use the notebook `data_collection.ipynb` to download datasets from the internet.

For training the hybrid approach of using OpenCLIP model to transform images into
vectors and feed the vectors to classical ML classifiers, you can download the
pre-encoded vectors from the following huggingface dataset [nazy-symbols-classification-openclip-encoded-image-data](https://huggingface.co/datasets/zhiwei2017/nazy-symbols-classification-openclip-encoded-image-data/tree/main).
It container the training data for binary classification, and multi-class classification.

## Prepare the dataset
Use the notebook `data_preprocessing.ipynb` to prepare the dataset for training.

## Train the model
To train the binary classification model, please use the following notebooks:

- `YOLO-binary.ipynb`: This notebook trains a YOLO model for binary classification.
- `ViT-binary.ipynb`: This notebook trains a Vision Transformer (ViT) model for binary classification.
- `ResNet-binary.ipynb`: This notebook trains a ResNet model for binary classification.
- `EfficientNet-binary.ipynb`: This notebook trains an EfficientNet model for binary classification.
- `OpenCLIP-transformer-binary.ipynb`: This notebook trains different classical ML classifiers for binary classification, with using OpenCLIP model to transform the image into a vector.

To train the multi-class classification model, please use the following notebooks:

- `YOLO-multi.ipynb`: This notebook trains a YOLO model for binary classification.
- `ViT-multi.ipynb`: This notebook trains a Vision Transformer (ViT) model for binary classification.
- `ResNet-multi.ipynb`: This notebook trains a ResNet model for binary classification.
- `EfficientNet-multi.ipynb`: This notebook trains an EfficientNet model for binary classification.
- `OpenCLIP-transformer-multi.ipynb`: This notebook trains different classical ML classifiers for binary classification, with using OpenCLIP model to transform the image into a vector.

Please note that for model `Moondream` and `OpenCLIP`, we do not train them. The notebooks
`Moondream-binary.ipynb` and `OpenCLIP-binary.ipynb` are used to evaluate the 
pre-trained models on the binary classification dataset. And the notebooks 
`Moondream-multi.ipynb` and `OpenCLIP-multi.ipynb` are used to evaluate the 
pre-trained models on the multi-class classification dataset.

### Train the model with custom dataset
To train the model with custom dataset, please follow the steps below:
1. Prepare the dataset in the format required by the model. The dataset should be organized into folders, with each folder containing images for a specific class.
2. Update the dataset path in the notebook to point to your custom dataset.
3. Run the corresponding notebook to train the model with your custom dataset. 
   - If you want to use the OpenCLIP model to transform the images into vectors, please make sure you have downloaded the pre-encoded vectors from the huggingface dataset mentioned above. 
   - For the hybrid approach, you can use the `OpenCLIP-transformer-binary.ipynb` or `OpenCLIP-transformer-multi.ipynb` notebooks, there are steps to help you to encode your images into dataframe, such that you can train the classical ML classifiers with the OpenCLIP encoded vectors.
4. After training, you can evaluate the model using the predefined code in the same training notebooks.

## Evaluate the model
The evaluation is done in the same training notebooks. After training the model, you can continue run the result of cells in the notebook to evaluate the model on the test dataset. The evaluation results will be printed in the notebook.

### Model Artifacts
The trained model artifacts will be saved in the huggingface repos [nazi-symbols-binary-classification](https://huggingface.co/zhiwei2017/nazi-symbols-binary-classification)
and [nazi-symbols-multi-class-classification](https://huggingface.co/zhiwei2017/nazi-symbols-multi-class-classification).

The current best performance model for binary classification is using OpenCLIP model as encoder pair with a SVC classifier,
and for multi-class classification is the YOLO model.