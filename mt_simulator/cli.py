"""Interfaz de línea de comandos del simulador."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .formatter import (
    Colors, colors_supported, describe_machine, format_result, format_summary,
    markdown_report, symbol_separator, transition_table, TURNSTILE,
)
from .parser import MTParseError, load_machine
from .simulator import DEFAULT_MAX_STEPS, SimulationResult, Simulator


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m mt_simulator",
        description="Simulador de Máquinas de Turing de una cinta (Proyecto 3 — Teoría de la Computación).",
    )
    p.add_argument("archivo", help="archivo YAML con la descripción formal de la MT")
    p.add_argument("-i", "--input", action="append", dest="inputs", metavar="CADENA",
                   help="simula esta cadena en lugar de las del YAML (se puede repetir)")
    p.add_argument("--max-steps", type=int, default=DEFAULT_MAX_STEPS,
                   help=f"límite de pasos para detectar ciclos (default {DEFAULT_MAX_STEPS})")
    p.add_argument("-t", "--table", action="store_true",
                   help="muestra la descripción formal y la tabla de transiciones δ")
    p.add_argument("-s", "--summary", action="store_true",
                   help="solo muestra el resumen (sin la lista de IDs)")
    p.add_argument("-p", "--step", action="store_true",
                   help="modo paso a paso: presione Enter para avanzar cada ID")
    p.add_argument("-o", "--output", metavar="ARCHIVO.md",
                   help="guarda un reporte Markdown con todas las IDs")
    p.add_argument("--no-color", action="store_true", help="desactiva los colores ANSI")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def _step_by_step(result: SimulationResult, sep: str, colors: Colors) -> None:
    print(colors.bold(f"Entrada: \"{result.input_string or 'ε'}\"  (Enter = siguiente, q = saltar)"))
    for d in result.ids:
        prefix = "   " if d.step == 0 else f" {TURNSTILE} "
        line = f"  {d.step:>4}{prefix}{d.render(sep)}"
        if d.transition is not None:
            line += colors.dim(f"      ({d.transition})")
        print(line, end="")
        try:
            if input().strip().lower() == "q":
                break
        except EOFError:
            print()
            break


def main(argv: Optional[List[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    colors = Colors(enabled=not args.no_color and colors_supported())

    try:
        machine = load_machine(args.archivo)
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{args.archivo}'", file=sys.stderr)
        return 2
    except MTParseError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    inputs = args.inputs if args.inputs else machine.inputs
    if not inputs:
        print("Error: no hay cadenas para simular (agregue 'inputs' al YAML o use --input)",
              file=sys.stderr)
        return 2

    print(colors.bold("=" * 72))
    print(describe_machine(machine))
    if args.table:
        print("\nFunciones de transición:")
        print(transition_table(machine))
    print(colors.bold("=" * 72))

    simulator = Simulator(machine, max_steps=args.max_steps)
    sep = symbol_separator(machine)
    results = []
    for s in inputs:
        result = simulator.run(s)
        results.append(result)
        print()
        if args.step:
            _step_by_step(result, sep, colors)
            print(format_result(result, machine, colors, show_ids=False))
        else:
            print(format_result(result, machine, colors, show_ids=not args.summary))

    print("\n" + colors.bold("Resumen"))
    print(format_summary(results, colors))

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown_report(machine, results), encoding="utf-8")
        print(f"\nReporte guardado en {out}")
    return 0
