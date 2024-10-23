from pydantic import BaseModel, Field
from random import SystemRandom
from typing import Callable, Sequence, Any, Tuple, Union, Dict, List

crypto_gen = SystemRandom()


class PipelineStep(BaseModel):
    name: str = Field(...,
                      description="",
                      examples=[])
    func: Callable = Field(..., description="", examples=[])
    func_params: Union[Dict[str, Any], None] = Field(..., description="", examples=[])


class Pipeline:
    def __init__(self, steps: Sequence[Tuple[str, Callable, Union[Dict[str, Any], None]]]):
        self._steps: List[PipelineStep] = []
        self.validate_steps(steps)

    def validate_steps(self, steps):
        for step in steps:
            name, func, func_params = step
            self._steps.append(PipelineStep(name=name, func=func,
                                            func_params=func_params))

    @property
    def steps(self):
        return self._steps

    def run(self, paths, skip_prob=0):
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
