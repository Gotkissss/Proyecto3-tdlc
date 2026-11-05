"""Cinta infinita en ambas direcciones y parsing de las cadenas de entrada."""

from __future__ import annotations

from typing import Dict, Iterable, List


def tokenize(text: str, alphabet: Iterable[str]) -> List[str]:
    """Convierte una cadena de entrada en una lista de símbolos.

    - Si la cadena tiene espacios, cada palabra es un símbolo ("a b c").
    - Si no, se usa *longest match* contra el alfabeto, lo que permite
      símbolos de más de un carácter.
    Lanza ``ValueError`` si encuentra un símbolo que no pertenece al alfabeto.
    """
    symbols = sorted(set(alphabet), key=len, reverse=True)
    if " " in text.strip():
        tokens = text.split()
        for tok in tokens:
            if tok not in symbols:
                raise ValueError(f"Símbolo '{tok}' no pertenece al alfabeto {sorted(symbols)}")
        return tokens

    tokens: List[str] = []
    i = 0
    while i < len(text):
        for sym in symbols:
            if sym and text.startswith(sym, i):
                tokens.append(sym)
                i += len(sym)
                break
        else:
            raise ValueError(
                f"Símbolo '{text[i]}' (posición {i}) no pertenece al alfabeto {sorted(symbols)}"
            )
    return tokens


class Tape:
    """Cinta de una MT: diccionario posición -> símbolo; lo ausente es blanco."""

    def __init__(self, symbols: Iterable[str], blank: str = "B") -> None:
        self.blank = blank
        self.cells: Dict[int, str] = {
            i: s for i, s in enumerate(symbols) if s != blank
        }
        self.head = 0

    def read(self) -> str:
        return self.cells.get(self.head, self.blank)

    def write(self, symbol: str) -> None:
        if symbol == self.blank:
            self.cells.pop(self.head, None)
        else:
            self.cells[self.head] = symbol

    def move(self, direction: str) -> None:
        if direction == "L":
            self.head -= 1
        elif direction == "R":
            self.head += 1
        elif direction != "S":
            raise ValueError(f"Movimiento inválido: {direction}")

    def bounds(self) -> tuple:
        """Rango [inicio, fin] que cubre el contenido no blanco y el cabezal."""
        positions = list(self.cells) + [self.head]
        return min(positions), max(positions)

    def snapshot(self) -> List[str]:
        """Contenido visible de la cinta (incluye la celda del cabezal)."""
        lo, hi = self.bounds()
        return [self.cells.get(i, self.blank) for i in range(lo, hi + 1)]

    def content(self) -> str:
        """Contenido final de la cinta sin blancos en los extremos."""
        if not self.cells:
            return ""
        lo, hi = min(self.cells), max(self.cells)
        return "".join(self.cells.get(i, self.blank) for i in range(lo, hi + 1))
