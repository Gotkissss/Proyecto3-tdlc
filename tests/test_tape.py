import pytest

from mt_simulator.tape import Tape, tokenize


def test_tokenize_caracter_por_caracter():
    assert tokenize("aabb", ["a", "b"]) == ["a", "a", "b", "b"]
    assert tokenize("", ["a"]) == []


def test_tokenize_simbolos_largos_y_espacios():
    assert tokenize("a1a1b", ["a", "a1", "b"]) == ["a1", "a1", "b"]
    assert tokenize("uno dos uno", ["uno", "dos"]) == ["uno", "dos", "uno"]


def test_tokenize_simbolo_invalido():
    with pytest.raises(ValueError, match="'c'"):
        tokenize("abc", ["a", "b"])


def test_cinta_infinita_en_ambas_direcciones():
    tape = Tape("ab", blank="B")
    assert tape.read() == "a"
    tape.move("L")
    assert tape.read() == "B"
    tape.write("X")
    assert tape.content() == "Xab"
    tape.move("R"); tape.move("R"); tape.move("R"); tape.move("R")
    assert tape.head == 3 and tape.read() == "B"
    assert tape.snapshot() == ["X", "a", "b", "B", "B"]


def test_escribir_blanco_borra():
    tape = Tape("ab")
    tape.write("B")
    assert tape.content() == "b"
    tape.move("S")
    assert tape.head == 0
    with pytest.raises(ValueError):
        tape.move("X")
