import pytest

from mt_simulator.parser import MTParseError, parse_yaml

BASE = """
mt:
  states: [q0, q1, qf]
  input_alphabet: [a, b]
  tape_alphabet: [a, b, X, B]
  initial_state: q0
  accept_states: [qf]
  transitions:
{transitions}
  inputs: ["ab"]
"""

OK_T = """    - {state: q0, read: [a, B], write: [a, X], move: R, next: q1}
    - {state: q1, read: [b, a], write: [B, b], move: R, next: qf}"""


def build(transitions=OK_T, **replace):
    text = BASE.format(transitions=transitions)
    for old, new in replace.items():
        text = text.replace(old, new)
    return text


def test_parse_ok_respeta_formato_del_enunciado():
    mt = parse_yaml(build())
    t = mt.transitions[0]
    # read: [cinta, memoria]; write: [memoria nueva, cinta]
    assert (t.read_symbol, t.read_memory) == ("a", "B")
    assert (t.write_memory, t.write_symbol) == ("a", "X")
    assert str(t) == "δ([q0, B], a) = ([q1, a], X, R)"
    assert mt.inputs == ["ab"]
    assert mt.uses_memory()


def test_forma_abreviada_escalar():
    mt = parse_yaml(build("    - {state: q0, read: a, write: X, move: r, next: qf}"))
    t = mt.transitions[0]
    assert (t.read_symbol, t.read_memory, t.write_memory, t.write_symbol, t.move) == (
        "a", "B", "B", "X", "R")


@pytest.mark.parametrize("transitions, mensaje", [
    ("    - {state: q9, read: [a, B], write: [B, a], move: R, next: q1}", "q9"),
    ("    - {state: q0, read: [a, B], write: [B, a], move: R, next: q9}", "q9"),
    ("    - {state: q0, read: [c, B], write: [B, a], move: R, next: q1}", "'c'"),
    ("    - {state: q0, read: [a, B], write: [B, a], move: U, next: q1}", "movimiento"),
    ("    - {state: q0, read: [a, B, X], write: [B, a], move: R, next: q1}", "2 elementos"),
    (OK_T + "\n    - {state: q0, read: [a, B], write: [B, b], move: L, next: qf}", "no determinista"),
])
def test_transiciones_invalidas(transitions, mensaje):
    with pytest.raises(MTParseError) as exc:
        parse_yaml(build(transitions))
    assert mensaje in str(exc.value)


def test_errores_de_definicion():
    with pytest.raises(MTParseError, match="estado inicial"):
        parse_yaml(build(**{"initial_state: q0": "initial_state: q7"}))
    with pytest.raises(MTParseError, match="Σ ⊆ Γ"):
        parse_yaml(build(**{"input_alphabet: [a, b]": "input_alphabet: [a, b, c]"}))
    with pytest.raises(MTParseError, match="blanco"):
        parse_yaml(build(**{"tape_alphabet: [a, b, X, B]": "tape_alphabet: [a, b, X]"}))
    with pytest.raises(MTParseError, match="'mt'"):
        parse_yaml("otra: cosa")
    with pytest.raises(MTParseError, match="mal formado"):
        parse_yaml("mt: [unclosed")
