"""Estructuras de datos que alojan la definición formal de una Máquina de Turing.

La MT del proyecto usa *almacenamiento en el control finito* (Hopcroft, Motwani y
Ullman, sección 8.3.1): cada estado es un par ``[q, m]`` donde ``q`` es el nombre
del estado y ``m`` es un símbolo de la cinta guardado en la "memoria" del control.

Formato del YAML (según el enunciado)::

    - state: q0
      read:  [a, B]   # [símbolo leído en la cinta, símbolo en memoria]
      write: [a, B]   # [nuevo símbolo en memoria, símbolo escrito en la cinta]
      move: R
      next: q1

equivale a  δ([q0, B], a) = ([q1, a], B, R).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

#: Movimientos válidos del cabezal: izquierda, derecha y quedarse (stay).
MOVES = ("L", "R", "S")

#: Símbolo blanco por defecto (como en el enunciado).
DEFAULT_BLANK = "B"


@dataclass(frozen=True)
class StateConfig:
    """Estado compuesto ``[q, m]``: nombre del estado + símbolo en memoria."""

    name: str
    memory: str

    def __str__(self) -> str:
        return f"[{self.name}, {self.memory}]"


@dataclass(frozen=True)
class Transition:
    """Una función de transición δ([state, memory], read) = ([next, new_memory], write, move)."""

    state: str
    read_symbol: str
    read_memory: str
    write_memory: str
    write_symbol: str
    move: str
    next_state: str

    @property
    def key(self) -> Tuple[str, str, str]:
        """Llave de búsqueda: (estado, memoria, símbolo leído)."""
        return (self.state, self.read_memory, self.read_symbol)

    def __str__(self) -> str:
        return (
            f"δ([{self.state}, {self.read_memory}], {self.read_symbol}) = "
            f"([{self.next_state}, {self.write_memory}], {self.write_symbol}, {self.move})"
        )


@dataclass
class TuringMachine:
    """Descripción formal M = (Q, Σ, Γ, δ, q0, B, F) más las cadenas a simular."""

    states: List[str]
    input_alphabet: List[str]
    tape_alphabet: List[str]
    initial_state: str
    accept_states: List[str]
    transitions: List[Transition]
    blank: str = DEFAULT_BLANK
    inputs: List[str] = field(default_factory=list)
    name: str = "MT"
    description: str = ""
    _delta: Dict[Tuple[str, str, str], Transition] = field(
        default_factory=dict, init=False, repr=False
    )

    def __post_init__(self) -> None:
        self._delta = {t.key: t for t in self.transitions}

    def delta(self, state: str, memory: str, symbol: str) -> Optional[Transition]:
        """Devuelve la transición aplicable o ``None`` si la MT se detiene."""
        return self._delta.get((state, memory, symbol))

    def is_accepting(self, state: str) -> bool:
        return state in self.accept_states

    @property
    def initial_config(self) -> StateConfig:
        """El estado inicial siempre arranca con la memoria en blanco: [q0, B]."""
        return StateConfig(self.initial_state, self.blank)

    def uses_memory(self) -> bool:
        """``True`` si alguna transición usa la memoria del control finito."""
        return any(
            t.read_memory != self.blank or t.write_memory != self.blank
            for t in self.transitions
        )
