from pydantic import BaseModel, Field
from typing import Callable, Sequence, Any, Tuple, Union


class PipelineStep(BaseModel):
    name: str = Field(...,
                      description="",
                      examples=[])
    func: Callable = Field(..., description="", examples=[])
    func_params: Union[Sequence[Any], None] = Field(..., description="", examples=[])


class Pipeline:
    def __init__(self, steps: Sequence[Tuple[str, Callable, Sequence[Any]]]):
        self._steps = []
        self.validate_steps(steps)

    def validate_steps(self, steps):
        for step in steps:
            name, func, func_params = step
            self._steps.append(PipelineStep(name=name, func=func,
                                            func_params=func_params))

    @property
    def steps(self):
        return self._steps

    def run(self, paths):
        for path in paths:
            for step in self._steps:
                if step.func_params:
                    step.func(path, *step.func_params)
                else:
                    step.func(path)
