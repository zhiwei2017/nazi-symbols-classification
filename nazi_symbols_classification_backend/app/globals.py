"""Module for declaring global variables centrally.

When you need to change the global variable's value in some functions, please
remember to use `global your_global_var` before assigning new values.
"""
from typing import Dict, Any

state: Dict[str, Any] = dict()
