"""Simulador de Máquinas de Turing de una cinta — Proyecto 3, Teoría de la Computación."""

__version__ = "1.0.0"

from .model import StateConfig, Transition, TuringMachine  # noqa: E402
from .parser import MTParseError, load_machine, parse_yaml  # noqa: E402
from .simulator import InstantaneousDescription, SimulationResult, Simulator, simulate  # noqa: E402

__all__ = [
    "StateConfig", "Transition", "TuringMachine",
    "MTParseError", "load_machine", "parse_yaml",
    "InstantaneousDescription", "SimulationResult", "Simulator", "simulate",
]
