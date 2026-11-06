"""Presentación de resultados: descripción formal, tabla δ, IDs y reportes Markdown."""

from __future__ import annotations

import os
import sys
from typing import List, Sequence

from .model import TuringMachine
from .simulator import SimulationResult

TURNSTILE = "⊢"


class Colors:
    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    def _wrap(self, code: str, text: str) -> str:
        return f"\033[{code}m{text}\033[0m" if self.enabled else text

    def bold(self, t: str) -> str: return self._wrap("1", t)
    def green(self, t: str) -> str: return self._wrap("1;32", t)
    def red(self, t: str) -> str: return self._wrap("1;31", t)
    def cyan(self, t: str) -> str: return self._wrap("36", t)
    def yellow(self, t: str) -> str: return self._wrap("33", t)
    def dim(self, t: str) -> str: return self._wrap("2", t)


def colors_supported() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.name == "nt":
        os.system("")  # habilita secuencias ANSI en la consola de Windows
    return sys.stdout.isatty()


def symbol_separator(machine: TuringMachine) -> str:
    """Si hay símbolos de más de un carácter, las IDs se separan con espacios."""
    return " " if any(len(s) > 1 for s in machine.tape_alphabet) else ""


# ---------------------------------------------------------------------- texto
def describe_machine(machine: TuringMachine) -> str:
    lines = [
        f"M = (Q, Σ, Γ, δ, q0, B, F)  —  {machine.name}",
        f"  Q  = {{{', '.join(machine.states)}}}",
        f"  Σ  = {{{', '.join(machine.input_alphabet)}}}",
        f"  Γ  = {{{', '.join(machine.tape_alphabet)}}}",
        f"  q0 = {machine.initial_state}   (estado inicial {machine.initial_config})",
        f"  B  = {machine.blank}",
        f"  F  = {{{', '.join(machine.accept_states)}}}",
        f"  |δ| = {len(machine.transitions)} transiciones",
    ]
    if machine.description:
        lines.insert(1, "  " + machine.description.replace("\n", "\n  "))
    return "\n".join(lines)


def transition_table(machine: TuringMachine) -> str:
    """Tabla con todas las funciones de transición en notación δ."""
    return "\n".join(f"  {i:>3}. {t}" for i, t in enumerate(machine.transitions, 1))


def format_result(result: SimulationResult, machine: TuringMachine,
                  colors: Colors, show_ids: bool = True) -> str:
    sep = symbol_separator(machine)
    shown = result.input_string if result.input_string else "ε"
    out: List[str] = [colors.bold(f"Entrada: \"{shown}\"")]
    if show_ids and result.ids:
        width = len(str(len(result.ids) - 1))
        for d in result.ids:
            prefix = "   " if d.step == 0 else f" {TURNSTILE} "
            line = f"{colors.dim(str(d.step).rjust(width))}{prefix}{d.render(sep)}"
            if d.transition is not None:
                line += colors.dim(f"      ({d.transition})")
            out.append("  " + line)
    verdict = colors.green(result.verdict) if result.accepted else colors.red(result.verdict)
    final_tape = result.final_tape if result.final_tape else "(cinta vacía)"
    out += [
        f"  Pasos: {result.steps}",
        f"  Configuración final: {result.ids[-1].render(sep) if result.ids else '-'}",
        f"  Contenido final de la cinta: {colors.cyan(final_tape)}",
        f"  Resultado: {verdict} — {result.reason}",
    ]
    return "\n".join(out)


def format_summary(results: Sequence[SimulationResult], colors: Colors) -> str:
    rows = [("Entrada", "Pasos", "Cinta final", "Resultado")]
    for r in results:
        rows.append((r.input_string or "ε", str(r.steps), r.final_tape or "(vacía)", r.verdict))
    widths = [max(len(row[i]) for row in rows) for i in range(4)]
    lines = []
    for n, row in enumerate(rows):
        cells = [row[i].ljust(widths[i]) for i in range(4)]
        if n > 0:
            cells[3] = (colors.green if row[3] == "ACEPTADA" else colors.red)(cells[3])
        lines.append("  " + " │ ".join(cells))
        if n == 0:
            lines.append("  " + "─┼─".join("─" * w for w in widths))
    return "\n".join(lines)


# ------------------------------------------------------------------ markdown
def markdown_report(machine: TuringMachine, results: Sequence[SimulationResult]) -> str:
    sep = symbol_separator(machine)
    md: List[str] = [f"# Reporte de simulación — {machine.name}", ""]
    if machine.description:
        md += [machine.description, ""]
    md += [
        "## Descripción formal", "",
        "| Componente | Valor |", "|---|---|",
        f"| Q | {{{', '.join(machine.states)}}} |",
        f"| Σ | {{{', '.join(machine.input_alphabet)}}} |",
        f"| Γ | {{{', '.join(machine.tape_alphabet)}}} |",
        f"| q0 | {machine.initial_state} |",
        f"| B | {machine.blank} |",
        f"| F | {{{', '.join(machine.accept_states)}}} |",
        "", "## Funciones de transición", "",
        "| # | Estado | Lee (cinta) | Memoria | Nuevo estado | Nueva memoria | Escribe | Mov. |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for i, t in enumerate(machine.transitions, 1):
        md.append(
            f"| {i} | {t.state} | `{t.read_symbol}` | `{t.read_memory}` | {t.next_state} | "
            f"`{t.write_memory}` | `{t.write_symbol}` | {t.move} |"
        )
    md += ["", "## Resumen", "", "| Entrada | Pasos | Cinta final | Resultado |", "|---|---:|---|---|"]
    for r in results:
        md.append(f"| `{r.input_string or 'ε'}` | {r.steps} | `{r.final_tape or '(vacía)'}` | **{r.verdict}** |")
    for r in results:
        md += ["", f"## Entrada `{r.input_string or 'ε'}`", "",
               f"**Resultado:** {r.verdict} — {r.reason}  ", f"**Pasos:** {r.steps}  ",
               f"**Cinta final:** `{r.final_tape or '(vacía)'}`", "", "```text"]
        for d in r.ids:
            prefix = "   " if d.step == 0 else f" {TURNSTILE} "
            md.append(f"{str(d.step).rjust(5)}{prefix}{d.render(sep)}")
        md.append("```")
    return "\n".join(md) + "\n"
