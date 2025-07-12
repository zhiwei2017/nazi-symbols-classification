import yaml
import enum
import os
import requests
import click
from pydantic import BaseModel, Field

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ModelType(str, enum.Enum):
    """Enumeration for model types."""
    yolo = "YOLO"
    svc = "SVC"


class ModelInfoItem(BaseModel):
    url: str = Field(..., description="URL of the model")
    type: ModelType = Field(..., description="Type of the model (e.g., 'svc', 'yolo')")
    local_path: str = Field(..., description="Local stored path to the model")


class ModelInfoSchema(BaseModel):
    first_layer_model: ModelInfoItem = Field(..., description="First layer model information")
    second_layer_model: ModelInfoItem = Field(..., description="Second layer model information")


class ModelInfo:
    """Class to handle model information."""

    def __init__(self, model_info_path: str):
        self.model_info_path = model_info_path
        self.model_info = self.load_model_info()

    def load_model_info(self) -> ModelInfoSchema:
        """Load model information from a YAML file."""
        with open(self.model_info_path, 'r', encoding='utf-8') as f:
            return ModelInfoSchema.model_validate(yaml.safe_load(f))

    def get_model_info(self) -> ModelInfoSchema:
        """Return the loaded model information."""
        return self.model_info


def download_model(url: str, output_path: str) -> None:
    """
    Download a model from a given URL and save it to the specified output path.

    Args:
        url (str): The URL of the model to download.
        output_path (str): The local path where the model will be saved.
    """
    # Replace '/blob/' with '/resolve/' in the URL for direct access
    direct_url = url.replace("/blob/", "/resolve/")

    response = requests.get(direct_url, allow_redirects=True)
    response.raise_for_status()  # Raise an error if download fails

    with open(output_path, "wb") as f:
        f.write(response.content)



@click.command()
@click.option(
    "--file", "-f",
    default=f"{root_dir}/model_info.yaml",
    help="Path to the model_info.yaml file",
    show_default=True
)
def download_models(file: str = f"{root_dir}/model_info.yaml") -> None:
    """Download models from the yaml file with given path.

    Args:
        file (str): path to the model info yaml file.

    Returns:
        None
    """
    mi = ModelInfo(file)
    click.echo(f"Downloading model from {mi.model_info.first_layer_model.url} to {mi.model_info.first_layer_model.local_path}.")
    download_model(mi.model_info.first_layer_model.url, mi.model_info.first_layer_model.local_path)
    click.echo(f"Downloading model from {mi.model_info.second_layer_model.url} to {mi.model_info.second_layer_model.local_path}.")
    download_model(mi.model_info.second_layer_model.url, mi.model_info.second_layer_model.local_path)
    click.echo("All models downloaded successfully.")
