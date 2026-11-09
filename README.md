# Proyecto 3 — Simulador de Máquinas de Turing

**Teoría de la Computación · Universidad del Valle de Guatemala · Noviembre 2025**

Simulador de Máquinas de Turing (MT) deterministas de **una cinta**. Lee la descripción
formal de la MT desde un archivo YAML, simula cada cadena configurada, muestra la lista
completa de **descripciones instantáneas (IDs)**, la configuración final de la cinta e
indica si la cadena fue **aceptada** o **rechazada**.

## Integrantes

| Usuario de GitHub | Carné |
|---|---|
| [@Gotkissss](https://github.com/Gotkissss) | 24903 |
| [@Dallycita](https://github.com/Dallycita) | 241035 |

## Contenido

```text
Proyecto3-tdlc/
├── mt_simulator/            # código fuente del simulador
│   ├── model.py             # estructuras de datos: TuringMachine, Transition, StateConfig
│   ├── parser.py            # parsing y validación del YAML
│   ├── tape.py              # cinta infinita + parsing de la cadena de entrada
│   ├── simulator.py         # motor de simulación y descripciones instantáneas
│   ├── formatter.py         # salida en consola y reportes Markdown
│   └── cli.py               # interfaz de línea de comandos
├── maquinas/
│   ├── reconocedora_ww.yaml           # MT reconocedora:  { ww | w ∈ {a,b}+ }
│   ├── alteradora_suma_binaria.yaml   # MT alteradora:    x+y  →  suma en binario
│   └── ejemplos/                      # YAML del enunciado y aⁿbⁿ
├── salidas/                 # reportes generados con todas las IDs
├── docs/
│   ├── arquitectura.md      # diseño del programa
│   └── maquinas.md          # descripción formal, tablas δ y diagramas de ambas MT
└── tests/                   # pruebas con pytest
```

## Requisitos e instalación

* Python **3.9 o superior**
* [PyYAML](https://pypi.org/project/PyYAML/) (y `pytest` para correr las pruebas)

```bash
git clone https://github.com/Gotkissss/Proyecto3-tdlc.git
cd Proyecto3-tdlc
python -m venv .venv
# Windows: .venv\Scripts\activate      Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
python -m mt_simulator <archivo.yaml> [opciones]
```

| Opción | Descripción |
|---|---|
| `-t`, `--table` | Muestra la descripción formal y todas las funciones de transición δ. |
| `-i CADENA`, `--input CADENA` | Simula esta cadena en lugar de las del YAML (se puede repetir). |
| `-s`, `--summary` | Solo muestra el resultado de cada cadena, sin la lista de IDs. |
| `-p`, `--step` | Modo paso a paso: presione Enter para avanzar una ID (`q` para saltar). |
| `-o ARCHIVO.md`, `--output ARCHIVO.md` | Guarda un reporte Markdown con la tabla δ y todas las IDs. |
| `--max-steps N` | Límite de pasos para detectar ciclos infinitos (100 000 por defecto). |
| `--no-color` | Desactiva los colores ANSI. |

### Ejemplos

```bash
# MT reconocedora con sus 6 cadenas (3 aceptadas y 3 rechazadas)
python -m mt_simulator maquinas/reconocedora_ww.yaml --table

# MT alteradora con sus 5 cadenas
python -m mt_simulator maquinas/alteradora_suma_binaria.yaml --table

# Probar otra cadena paso a paso
python -m mt_simulator maquinas/reconocedora_ww.yaml -i abbabb --step

# Generar el reporte con todas las IDs
python -m mt_simulator maquinas/alteradora_suma_binaria.yaml -o salidas/reporte_suma_binaria.md
```

Salida (recortada):

```text
Entrada: "101+11"
   0   [q0, B]101+11
   1 ⊢ 1[q1, B]01+11      (δ([q0, B], 1) = ([q1, B], 1, R))
   2 ⊢ 10[q1, B]1+11      (δ([q1, B], 0) = ([q1, B], 0, R))
  ...
  53 ⊢ [qf, B]1000      (δ([home2, B], B) = ([qf, B], B, R))
  Pasos: 53
  Configuración final: [qf, B]1000
  Contenido final de la cinta: 1000
  Resultado: ACEPTADA — La MT se detuvo en el estado de aceptación [qf, B]
```

## Formato del archivo YAML

```yaml
mt:
  name: "Mi MT"                  # opcional
  description: "Qué hace"        # opcional
  blank: B                       # opcional, B por defecto
  states: [q0, q1, q2, qf]
  input_alphabet: [a, b]
  tape_alphabet: [a, b, B, X, Y]
  initial_state: q0
  accept_states: [qf]
  transitions:
    - state: q0
      read: [a, B]     # [símbolo leído en la cinta, símbolo en memoria]
      write: [a, B]    # [nuevo símbolo en memoria, símbolo escrito en la cinta]
      move: R          # L, R o S (quedarse)
      next: q1
  inputs:
    - "aabb"
    - "ab"
```

La transición anterior es **δ([q0, B], a) = ([q1, a], B, R)**: el estado de la MT es un
par `[q, m]` donde `m` es un símbolo guardado en el control finito (memoria), que siempre
empieza en blanco. Si una MT no necesita memoria se puede escribir `read: a` y
`write: X` (equivalen a `[a, B]` y `[B, X]`).

El parser valida que los estados existan, que `Σ ⊆ Γ`, que `B ∈ Γ`, que todos los
símbolos de las transiciones estén en Γ, que los movimientos sean válidos y que la MT
sea **determinista**. Si hay errores los reporta todos juntos.

### Criterio de aceptación

* Si la MT entra a un estado de `accept_states` se detiene y la cadena es **ACEPTADA**.
* Si no existe transición para la configuración actual, la MT se detiene y la cadena es **RECHAZADA**.
* Si se supera `--max-steps` la simulación se corta y la cadena se reporta como **RECHAZADA** (posible ciclo infinito).

## Máquinas del proyecto

Toda la información (descripción formal, tablas de transición, diagramas y explicación)
está en [`docs/maquinas.md`](docs/maquinas.md). Las IDs completas de cada cadena están en
[`salidas/`](salidas).

### 1. MT reconocedora — `{ ww | w ∈ {a,b}⁺ }`

Lenguaje **no libre de contexto**. La MT encuentra la mitad de la cadena marcando
alternadamente los extremos y luego compara ambas mitades llevando cada símbolo en la
**memoria del estado** (`[q7, a]` / `[q7, b]`). 10 estados, 39 transiciones.

| Cadena | Resultado |
|---|---|
| `abaaba`, `babbbabb`, `aabbaabb` | ACEPTADAS |
| `abaab`, `abbaab`, `aabbab` | RECHAZADAS |

### 2. MT alteradora — suma binaria

Transforma `x+y` en el resultado de la suma: decrementa `y` (con préstamo) e incrementa
`x` (con acarreo) hasta que `y = 0`, y luego borra `+y`. 12 estados, 32 transiciones.

| Entrada | Cinta final |
|---|---|
| `101+11` | `1000` |
| `1011+110` | `10001` |
| `111+111` | `1110` |
| `1+1111` | `10000` |
| `1100+0` | `1100` |

## Arquitectura

Ver [`docs/arquitectura.md`](docs/arquitectura.md). En resumen:
`parser.py` convierte el YAML en un objeto `TuringMachine` (`model.py`), `tape.py`
convierte la cadena en una cinta infinita, `simulator.py` aplica δ paso a paso guardando
cada ID en un `SimulationResult`, y `formatter.py`/`cli.py` lo muestran.

## Pruebas

```bash
python -m pytest
```

Incluye pruebas del parser, la cinta y el simulador, y verifica **exhaustivamente** las
dos MT: la reconocedora contra todas las cadenas de `{a,b}` de longitud ≤ 10 y la
alteradora contra todas las sumas `a + b` con `0 ≤ a, b < 20`.

## Video

Enlace al video (YouTube, no listado): _pendiente_
