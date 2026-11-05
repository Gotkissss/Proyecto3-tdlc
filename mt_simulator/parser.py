"""Parsing y validación del archivo YAML que describe la MT."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Union

import yaml

from .model import DEFAULT_BLANK, MOVES, Transition, TuringMachine


class MTParseError(ValueError):
    """Error en la descripción formal de la MT."""


def _as_list(value: Any, field_name: str) -> List[str]:
    if value is None:
        raise MTParseError(f"Falta el campo obligatorio '{field_name}'")
    if not isinstance(value, list):
        raise MTParseError(f"'{field_name}' debe ser una lista, se recibió: {value!r}")
    return [str(v) for v in value]


def _pair(value: Any, field_name: str, index: int, blank: str) -> List[str]:
    """``read``/``write`` son pares; un escalar se interpreta como sin memoria.

    - read:  escalar ``a``  ->  [a, B]   (símbolo de cinta, memoria en blanco)
    - write: escalar ``X``  ->  [B, X]   (memoria en blanco, escribe X)
    """
    if isinstance(value, list):
        if len(value) != 2:
            raise MTParseError(
                f"Transición #{index}: '{field_name}' debe tener 2 elementos, tiene {len(value)}"
            )
        return [str(value[0]), str(value[1])]
    if value is None:
        raise MTParseError(f"Transición #{index}: falta '{field_name}'")
    if field_name == "read":
        return [str(value), blank]
    return [blank, str(value)]


def parse_dict(data: Dict[str, Any], name: str = "MT") -> TuringMachine:
    """Construye y valida una :class:`TuringMachine` desde el diccionario del YAML."""
    if not isinstance(data, dict) or "mt" not in data:
        raise MTParseError("El YAML debe tener una llave raíz 'mt'")
    mt = data["mt"]
    if not isinstance(mt, dict):
        raise MTParseError("'mt' debe ser un diccionario")

    blank = str(mt.get("blank", DEFAULT_BLANK))
    states = _as_list(mt.get("states"), "states")
    input_alphabet = _as_list(mt.get("input_alphabet"), "input_alphabet")
    tape_alphabet = _as_list(mt.get("tape_alphabet"), "tape_alphabet")
    accept_states = _as_list(mt.get("accept_states"), "accept_states")
    if mt.get("initial_state") is None:
        raise MTParseError("Falta el campo obligatorio 'initial_state'")
    initial_state = str(mt["initial_state"])

    errors: List[str] = []
    state_set, tape_set = set(states), set(tape_alphabet)

    if len(state_set) != len(states):
        errors.append("Hay estados repetidos en 'states'")
    if initial_state not in state_set:
        errors.append(f"El estado inicial '{initial_state}' no está en 'states'")
    for q in accept_states:
        if q not in state_set:
            errors.append(f"El estado de aceptación '{q}' no está en 'states'")
    if blank not in tape_set:
        errors.append(f"El símbolo blanco '{blank}' debe pertenecer a 'tape_alphabet'")
    if blank in input_alphabet:
        errors.append(f"El símbolo blanco '{blank}' no puede estar en 'input_alphabet'")
    for s in input_alphabet:
        if s not in tape_set:
            errors.append(f"El símbolo de entrada '{s}' no está en 'tape_alphabet' (Σ ⊆ Γ)")

    raw_transitions = mt.get("transitions") or []
    if not isinstance(raw_transitions, list):
        errors.append("'transitions' debe ser una lista")
        raw_transitions = []

    transitions: List[Transition] = []
    seen: Dict[tuple, int] = {}
    for i, raw in enumerate(raw_transitions, start=1):
        if not isinstance(raw, dict):
            errors.append(f"Transición #{i}: debe ser un diccionario")
            continue
        try:
            read_sym, read_mem = _pair(raw.get("read"), "read", i, blank)
            write_mem, write_sym = _pair(raw.get("write"), "write", i, blank)
        except MTParseError as exc:
            errors.append(str(exc))
            continue
        state = str(raw.get("state"))
        nxt = str(raw.get("next"))
        move = str(raw.get("move", "")).upper()

        if state not in state_set:
            errors.append(f"Transición #{i}: estado '{state}' no existe")
        if nxt not in state_set:
            errors.append(f"Transición #{i}: estado siguiente '{nxt}' no existe")
        if move not in MOVES:
            errors.append(f"Transición #{i}: movimiento '{move}' inválido (use L, R o S)")
        for label, sym in (
            ("símbolo leído", read_sym),
            ("memoria leída", read_mem),
            ("memoria escrita", write_mem),
            ("símbolo escrito", write_sym),
        ):
            if sym not in tape_set:
                errors.append(f"Transición #{i}: {label} '{sym}' no está en 'tape_alphabet'")

        t = Transition(state, read_sym, read_mem, write_mem, write_sym, move, nxt)
        if t.key in seen:
            errors.append(
                f"Transición #{i}: no determinista, choca con la #{seen[t.key]} "
                f"para δ([{state}, {read_mem}], {read_sym})"
            )
        else:
            seen[t.key] = i
        transitions.append(t)

    if not transitions:
        errors.append("La MT no tiene funciones de transición")

    inputs = [("" if s is None else str(s)) for s in (mt.get("inputs") or [])]

    if errors:
        raise MTParseError("Descripción de la MT inválida:\n  - " + "\n  - ".join(errors))

    return TuringMachine(
        states=states,
        input_alphabet=input_alphabet,
        tape_alphabet=tape_alphabet,
        initial_state=initial_state,
        accept_states=accept_states,
        transitions=transitions,
        blank=blank,
        inputs=inputs,
        name=str(mt.get("name", name)),
        description=str(mt.get("description", "")).strip(),
    )


def parse_yaml(text: str, name: str = "MT") -> TuringMachine:
    """Parsea el texto de un YAML."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise MTParseError(f"YAML mal formado: {exc}") from exc
    return parse_dict(data, name=name)


def load_machine(path: Union[str, Path]) -> TuringMachine:
    """Carga una MT desde un archivo ``.yaml``."""
    path = Path(path)
    return parse_yaml(path.read_text(encoding="utf-8"), name=path.stem)
