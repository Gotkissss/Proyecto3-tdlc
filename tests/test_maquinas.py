"""Pruebas de las MT entregadas, incluyendo verificación exhaustiva."""

from itertools import product
from pathlib import Path

import pytest

from mt_simulator import load_machine, simulate

MAQUINAS = Path(__file__).resolve().parent.parent / "maquinas"


@pytest.fixture(scope="module")
def ww():
    return load_machine(MAQUINAS / "reconocedora_ww.yaml")


@pytest.fixture(scope="module")
def suma():
    return load_machine(MAQUINAS / "alteradora_suma_binaria.yaml")


def es_ww(s: str) -> bool:
    n = len(s)
    return n > 0 and n % 2 == 0 and s[: n // 2] == s[n // 2:]


def test_ww_cadenas_del_video(ww):
    esperados = {"abaaba": True, "babbbabb": True, "aabbaabb": True,
                 "abaab": False, "abbaab": False, "aabbab": False}
    for s, ok in esperados.items():
        assert len(s) >= 5
        assert simulate(ww, s).accepted is ok, s


def test_ww_exhaustivo_hasta_longitud_10(ww):
    for n in range(0, 11):
        for letras in product("ab", repeat=n):
            s = "".join(letras)
            assert simulate(ww, s).accepted == es_ww(s), s


def test_suma_cadenas_del_video(suma):
    for s in suma.inputs:
        assert len(s) >= 5
        x, y = s.split("+")
        r = simulate(suma, s)
        assert r.accepted
        assert r.final_tape == bin(int(x, 2) + int(y, 2))[2:]
        assert str(r.ids[-1]).startswith("[qf, B]")


def test_suma_exhaustiva(suma):
    for a in range(0, 20):
        for b in range(0, 20):
            s = f"{a:b}+{b:b}"
            r = simulate(suma, s)
            assert r.accepted and int(r.final_tape, 2) == a + b, s


def test_suma_conserva_ceros_a_la_izquierda(suma):
    assert simulate(suma, "0011+1").final_tape == "0100"


@pytest.mark.parametrize("s", ["", "+1", "1+", "1+1+1", "11", "+"])
def test_suma_rechaza_entradas_mal_formadas(suma, s):
    assert not simulate(suma, s).accepted


def test_ejemplos_cargan():
    for path in (MAQUINAS / "ejemplos").glob("*.yaml"):
        mt = load_machine(path)
        for s in mt.inputs:
            simulate(mt, s)


def test_anbn():
    mt = load_machine(MAQUINAS / "ejemplos" / "anbn.yaml")
    resultados = {s: simulate(mt, s).accepted for s in mt.inputs}
    assert resultados == {"aabb": True, "aaabbb": True, "aab": False, "abab": False}
