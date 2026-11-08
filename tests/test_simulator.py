from mt_simulator.parser import parse_yaml
from mt_simulator.simulator import simulate

LOOP = """
mt:
  states: [q0, qf]
  input_alphabet: [a]
  tape_alphabet: [a, B]
  initial_state: q0
  accept_states: [qf]
  transitions:
    - {state: q0, read: a, write: a, move: S, next: q0}
"""

MEMORIA = """
mt:
  states: [q0, q1, qf]
  input_alphabet: [a, b]
  tape_alphabet: [a, b, B]
  initial_state: q0
  accept_states: [qf]
  transitions:
    # guarda el primer símbolo en memoria y lo copia al final de la cadena
    - {state: q0, read: [a, B], write: [a, a], move: R, next: q1}
    - {state: q0, read: [b, B], write: [b, b], move: R, next: q1}
    - {state: q1, read: [a, a], write: [a, a], move: R, next: q1}
    - {state: q1, read: [b, a], write: [a, b], move: R, next: q1}
    - {state: q1, read: [a, b], write: [b, a], move: R, next: q1}
    - {state: q1, read: [b, b], write: [b, b], move: R, next: q1}
    - {state: q1, read: [B, a], write: [B, a], move: S, next: qf}
    - {state: q1, read: [B, b], write: [B, b], move: S, next: qf}
"""


def test_ids_y_memoria():
    mt = parse_yaml(MEMORIA)
    r = simulate(mt, "ab")
    assert r.accepted
    assert [str(d) for d in r.ids] == [
        "[q0, B]ab",
        "a[q1, a]b",
        "ab[q1, a]B",
        "ab[qf, B]a",
    ]
    assert r.final_tape == "aba"
    assert r.steps == 3
    assert r.ids[1].transition is mt.transitions[0]


def test_rechazo_por_falta_de_transicion():
    r = simulate(parse_yaml(MEMORIA), "")
    assert not r.accepted and r.steps == 0
    assert "No existe δ([q0, B], B)" in r.reason


def test_entrada_fuera_del_alfabeto():
    r = simulate(parse_yaml(MEMORIA), "abc")
    assert not r.accepted and "Entrada inválida" in r.reason


def test_limite_de_pasos():
    r = simulate(parse_yaml(LOOP), "a", max_steps=50)
    assert not r.accepted and not r.halted
    assert r.steps == 50 and "límite" in r.reason
