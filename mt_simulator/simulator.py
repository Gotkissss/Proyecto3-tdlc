"""Motor de simulación: aplica δ paso a paso y registra las descripciones instantáneas."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .model import StateConfig, Transition, TuringMachine
from .tape import Tape, tokenize

DEFAULT_MAX_STEPS = 100_000


@dataclass(frozen=True)
class InstantaneousDescription:
    """ID de la MT: α [q, m] β  (el cabezal está sobre el primer símbolo de β)."""

    step: int
    config: StateConfig
    left: tuple
    right: tuple
    transition: Optional[Transition] = None  # transición que produjo esta ID

    def render(self, sep: str = "") -> str:
        left = sep.join(self.left)
        right = sep.join(self.right)
        state = str(self.config)
        if sep:
            return " ".join(p for p in (left, state, right) if p)
        return f"{left}{state}{right}"

    def __str__(self) -> str:
        return self.render()


class Verdict:
    ACCEPTED = "ACEPTADA"
    REJECTED = "RECHAZADA"


@dataclass
class SimulationResult:
    input_string: str
    accepted: bool
    reason: str
    ids: List[InstantaneousDescription] = field(default_factory=list)
    final_tape: str = ""
    final_config: Optional[StateConfig] = None
    halted: bool = True

    @property
    def steps(self) -> int:
        return max(len(self.ids) - 1, 0)

    @property
    def verdict(self) -> str:
        return Verdict.ACCEPTED if self.accepted else Verdict.REJECTED


class Simulator:
    """Simula una MT determinista de una cinta con memoria en el control finito.

    Criterio de parada (Hopcroft):
      * Si la MT entra a un estado de aceptación se detiene y ACEPTA.
      * Si no existe δ para la configuración actual se detiene y RECHAZA.
      * Si se supera ``max_steps`` se corta la simulación y se RECHAZA
        (posible ciclo infinito).
    """

    def __init__(self, machine: TuringMachine, max_steps: int = DEFAULT_MAX_STEPS) -> None:
        self.machine = machine
        self.max_steps = max_steps

    # ------------------------------------------------------------------ helpers
    def _make_tape(self, input_string: str) -> Tape:
        symbols = tokenize(input_string, self.machine.input_alphabet)
        return Tape(symbols, blank=self.machine.blank)

    def _snapshot(self, step: int, config: StateConfig, tape: Tape,
                  transition: Optional[Transition]) -> InstantaneousDescription:
        lo, _ = tape.bounds()
        cells = tape.snapshot()
        idx = tape.head - lo
        left = tuple(cells[:idx])
        right = tuple(cells[idx:])
        # Como en el libro, se omiten los blancos de los extremos salvo el de
        # la celda del cabezal.
        blank = self.machine.blank
        while left and left[0] == blank:
            left = left[1:]
        while len(right) > 1 and right[-1] == blank:
            right = right[:-1]
        return InstantaneousDescription(step, config, left, right, transition)

    # ------------------------------------------------------------------ API
    def run(self, input_string: str) -> SimulationResult:
        machine = self.machine
        try:
            tape = self._make_tape(input_string)
        except ValueError as exc:
            return SimulationResult(input_string, False, f"Entrada inválida: {exc}")

        config = machine.initial_config
        ids = [self._snapshot(0, config, tape, None)]
        step = 0

        while True:
            if machine.is_accepting(config.name):
                return SimulationResult(
                    input_string, True,
                    f"La MT se detuvo en el estado de aceptación {config}",
                    ids, tape.content(), config,
                )
            symbol = tape.read()
            t = machine.delta(config.name, config.memory, symbol)
            if t is None:
                return SimulationResult(
                    input_string, False,
                    f"No existe δ({config}, {symbol}); la MT se detuvo en un estado de no aceptación",
                    ids, tape.content(), config,
                )
            if step >= self.max_steps:
                return SimulationResult(
                    input_string, False,
                    f"Se alcanzó el límite de {self.max_steps} pasos (posible ciclo infinito)",
                    ids, tape.content(), config, halted=False,
                )
            tape.write(t.write_symbol)
            tape.move(t.move)
            config = StateConfig(t.next_state, t.write_memory)
            step += 1
            ids.append(self._snapshot(step, config, tape, t))


def simulate(machine: TuringMachine, input_string: str,
             max_steps: int = DEFAULT_MAX_STEPS) -> SimulationResult:
    """Atajo para simular una sola cadena."""
    return Simulator(machine, max_steps).run(input_string)
