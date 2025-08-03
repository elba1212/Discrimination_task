"""
Faces Discrimination Experiment Package

A Python package for conducting face discrimination psychological experiments.
Converted from MATLAB PsychToolbox implementation.
"""

__version__ = "1.0.0"
__author__ = "Converted from MATLAB"

from .main import run_experiment
from .discrimination_test import FacesDiscriminationTest
from .training import TrainingDiscriminationTest
from .config import ExperimentConfig
from .utils import PathManager, Logger

__all__ = [
    "run_experiment",
    "FacesDiscriminationTest", 
    "TrainingDiscriminationTest",
    "ExperimentConfig",
    "PathManager",
    "Logger"
]