from pydantic import BaseModel, Field
from random import SystemRandom
from typing import Callable, Sequence, Any, Tuple, Union, Dict, List

crypto_gen = SystemRandom()


class PipelineStep(BaseModel):
    """
    Represents a single step in the image processing pipeline.

    Attributes:
        name (str): The name of the step.
        func (Callable): The function to execute for this step.
        func_params (Union[Dict[str, Any], None]): Optional parameters to pass to the function.
    """
    name: str = Field(
        ...,
        description="The name of the pipeline step.",
        examples=["resize_image", "blur_image"]
    )
    func: Callable = Field(
        ...,
        description="The function to execute during this step.",
        examples=[]
    )
    func_params: Union[Dict[str, Any], None] = Field(
        ...,
        description="Optional parameters for the function.",
        examples=[{"width": 100, "height": 200}]
    )


class Pipeline:
    """
    A class to manage and execute a sequence of image processing steps.

    Attributes:
        _steps (List[PipelineStep]): Internal list of pipeline steps.

    Methods:
        __init__(steps): Initializes the pipeline with the given steps.
        validate_steps(steps): Validates and stores the steps in the pipeline.
        steps: Returns the list of pipeline steps.
        run(paths, skip_prob): Executes the pipeline on a list of file paths.
    """

    def __init__(self,
                 steps: Sequence[Tuple[str, Callable, Union[Dict[str, Any], None]]]) -> None:
        """
        Initializes the Pipeline object with a sequence of steps.

        Args:
            steps (Sequence[Tuple[str, Callable, Union[Dict[str, Any], None]]]):
                A sequence of tuples where each tuple contains:
                - name (str): The name of the step.
                - func (Callable): The function to execute for this step.
                - func_params (Union[Dict[str, Any], None]): Optional parameters for the function.

        Returns:
            None
        """
        self._steps: List[PipelineStep] = []
        self.validate_steps(steps)

    def validate_steps(self,
                       steps: Sequence[Tuple[str, Callable, Union[Dict[str, Any], None]]]) -> None:
        """
        Validates and stores the pipeline steps.

        Args:
            steps (Sequence[Tuple[str, Callable, Union[Dict[str, Any], None]]]):
                A sequence of tuples where each tuple contains:
                - name (str): The name of the step.
                - func (Callable): The function to execute for this step.
                - func_params (Union[Dict[str, Any], None]): Optional parameters for the function.

        Returns:
            None
        """
        for step in steps:
            name, func, func_params = step
            self._steps.append(PipelineStep(name=name, func=func, func_params=func_params))

    @property
    def steps(self) -> List[PipelineStep]:
        """
        Returns the list of pipeline steps.

        Returns:
            List[PipelineStep]: The list of steps in the pipeline.
        """
        return self._steps

    def run(self, paths: List[str], skip_prob: float = 0) -> None:
        """
        Executes the pipeline on a list of file paths.

        Args:
            paths (List[str]): A list of file paths to process.
            skip_prob (float, optional): The probability of skipping a step. Defaults to 0.
                Must be in the range [0, 1).

        Raises:
            ValueError: If `skip_prob` is not in the range [0, 1).

        Returns:
            None
        """
        if not 0 <= skip_prob < 1:
            raise ValueError("skip_prob should be in the interval [0, 1).")
        for path in paths:
            for step in self._steps:
                if skip_prob and crypto_gen.uniform(0, 1) < skip_prob:
                    continue
                elif step.func_params:
                    step.func(path, **step.func_params)
                else:
                    step.func(path)
