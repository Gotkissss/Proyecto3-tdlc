# Reporte de simulación — Reconocedora ww

Reconoce L = { ww | w ∈ {a,b}+ } (lenguaje no libre de contexto) usando memoria en el control finito.

## Descripción formal

| Componente | Valor |
|---|---|
| Q | {q0, q1, q2, q3, q4, q5, q6, q7, q8, qf} |
| Σ | {a, b} |
| Γ | {a, b, x, y, Z, B} |
| q0 | q0 |
| B | B |
| F | {qf} |

## Funciones de transición

| # | Estado | Lee (cinta) | Memoria | Nuevo estado | Nueva memoria | Escribe | Mov. |
|---:|---|---|---|---|---|---|---|
| 1 | q0 | `a` | `B` | q1 | `B` | `x` | R |
| 2 | q0 | `b` | `B` | q1 | `B` | `y` | R |
| 3 | q0 | `x` | `B` | q4 | `B` | `a` | R |
| 4 | q0 | `y` | `B` | q4 | `B` | `b` | R |
| 5 | q1 | `a` | `B` | q1 | `B` | `a` | R |
| 6 | q1 | `b` | `B` | q1 | `B` | `b` | R |
| 7 | q1 | `x` | `B` | q2 | `B` | `x` | L |
| 8 | q1 | `y` | `B` | q2 | `B` | `y` | L |
| 9 | q1 | `B` | `B` | q2 | `B` | `B` | L |
| 10 | q2 | `a` | `B` | q3 | `B` | `x` | L |
| 11 | q2 | `b` | `B` | q3 | `B` | `y` | L |
| 12 | q3 | `a` | `B` | q3 | `B` | `a` | L |
| 13 | q3 | `b` | `B` | q3 | `B` | `b` | L |
| 14 | q3 | `x` | `B` | q0 | `B` | `x` | R |
| 15 | q3 | `y` | `B` | q0 | `B` | `y` | R |
| 16 | q4 | `x` | `B` | q4 | `B` | `a` | R |
| 17 | q4 | `y` | `B` | q4 | `B` | `b` | R |
| 18 | q4 | `B` | `B` | q5 | `B` | `B` | L |
| 19 | q5 | `a` | `B` | q5 | `B` | `a` | L |
| 20 | q5 | `b` | `B` | q5 | `B` | `b` | L |
| 21 | q5 | `x` | `B` | q5 | `B` | `x` | L |
| 22 | q5 | `y` | `B` | q5 | `B` | `y` | L |
| 23 | q5 | `B` | `B` | q6 | `B` | `B` | R |
| 24 | q6 | `Z` | `B` | q6 | `B` | `Z` | R |
| 25 | q6 | `x` | `B` | q7 | `a` | `Z` | R |
| 26 | q6 | `y` | `B` | q7 | `b` | `Z` | R |
| 27 | q6 | `B` | `B` | qf | `B` | `B` | S |
| 28 | q7 | `x` | `a` | q7 | `a` | `x` | R |
| 29 | q7 | `y` | `a` | q7 | `a` | `y` | R |
| 30 | q7 | `Z` | `a` | q7 | `a` | `Z` | R |
| 31 | q7 | `a` | `a` | q8 | `B` | `Z` | L |
| 32 | q7 | `x` | `b` | q7 | `b` | `x` | R |
| 33 | q7 | `y` | `b` | q7 | `b` | `y` | R |
| 34 | q7 | `Z` | `b` | q7 | `b` | `Z` | R |
| 35 | q7 | `b` | `b` | q8 | `B` | `Z` | L |
| 36 | q8 | `Z` | `B` | q8 | `B` | `Z` | L |
| 37 | q8 | `x` | `B` | q8 | `B` | `x` | L |
| 38 | q8 | `y` | `B` | q8 | `B` | `y` | L |
| 39 | q8 | `B` | `B` | q6 | `B` | `B` | R |

## Resumen

| Entrada | Pasos | Cinta final | Resultado |
|---|---:|---|---|
| `abaaba` | 75 | `ZZZZZZ` | **ACEPTADA** |
| `babbbabb` | 119 | `ZZZZZZZZ` | **ACEPTADA** |
| `aabbaabb` | 119 | `ZZZZZZZZ` | **ACEPTADA** |
| `abaab` | 20 | `xyxxy` | **RECHAZADA** |
| `abbaab` | 50 | `ZZyZab` | **RECHAZADA** |
| `aabbab` | 41 | `Zxybab` | **RECHAZADA** |

## Entrada `abaaba`

**Resultado:** ACEPTADA — La MT se detuvo en el estado de aceptación [qf, B]  
**Pasos:** 75  
**Cinta final:** `ZZZZZZ`

```text
    0   [q0, B]abaaba
    1 ⊢ x[q1, B]baaba
    2 ⊢ xb[q1, B]aaba
    3 ⊢ xba[q1, B]aba
    4 ⊢ xbaa[q1, B]ba
    5 ⊢ xbaab[q1, B]a
    6 ⊢ xbaaba[q1, B]B
    7 ⊢ xbaab[q2, B]a
    8 ⊢ xbaa[q3, B]bx
    9 ⊢ xba[q3, B]abx
   10 ⊢ xb[q3, B]aabx
   11 ⊢ x[q3, B]baabx
   12 ⊢ [q3, B]xbaabx
   13 ⊢ x[q0, B]baabx
   14 ⊢ xy[q1, B]aabx
   15 ⊢ xya[q1, B]abx
   16 ⊢ xyaa[q1, B]bx
   17 ⊢ xyaab[q1, B]x
   18 ⊢ xyaa[q2, B]bx
   19 ⊢ xya[q3, B]ayx
   20 ⊢ xy[q3, B]aayx
   21 ⊢ x[q3, B]yaayx
   22 ⊢ xy[q0, B]aayx
   23 ⊢ xyx[q1, B]ayx
   24 ⊢ xyxa[q1, B]yx
   25 ⊢ xyx[q2, B]ayx
   26 ⊢ xy[q3, B]xxyx
   27 ⊢ xyx[q0, B]xyx
   28 ⊢ xyxa[q4, B]yx
   29 ⊢ xyxab[q4, B]x
   30 ⊢ xyxaba[q4, B]B
   31 ⊢ xyxab[q5, B]a
   32 ⊢ xyxa[q5, B]ba
   33 ⊢ xyx[q5, B]aba
   34 ⊢ xy[q5, B]xaba
   35 ⊢ x[q5, B]yxaba
   36 ⊢ [q5, B]xyxaba
   37 ⊢ [q5, B]Bxyxaba
   38 ⊢ [q6, B]xyxaba
   39 ⊢ Z[q7, a]yxaba
   40 ⊢ Zy[q7, a]xaba
   41 ⊢ Zyx[q7, a]aba
   42 ⊢ Zy[q8, B]xZba
   43 ⊢ Z[q8, B]yxZba
   44 ⊢ [q8, B]ZyxZba
   45 ⊢ [q8, B]BZyxZba
   46 ⊢ [q6, B]ZyxZba
   47 ⊢ Z[q6, B]yxZba
   48 ⊢ ZZ[q7, b]xZba
   49 ⊢ ZZx[q7, b]Zba
   50 ⊢ ZZxZ[q7, b]ba
   51 ⊢ ZZx[q8, B]ZZa
   52 ⊢ ZZ[q8, B]xZZa
   53 ⊢ Z[q8, B]ZxZZa
   54 ⊢ [q8, B]ZZxZZa
   55 ⊢ [q8, B]BZZxZZa
   56 ⊢ [q6, B]ZZxZZa
   57 ⊢ Z[q6, B]ZxZZa
   58 ⊢ ZZ[q6, B]xZZa
   59 ⊢ ZZZ[q7, a]ZZa
   60 ⊢ ZZZZ[q7, a]Za
   61 ⊢ ZZZZZ[q7, a]a
   62 ⊢ ZZZZ[q8, B]ZZ
   63 ⊢ ZZZ[q8, B]ZZZ
   64 ⊢ ZZ[q8, B]ZZZZ
   65 ⊢ Z[q8, B]ZZZZZ
   66 ⊢ [q8, B]ZZZZZZ
   67 ⊢ [q8, B]BZZZZZZ
   68 ⊢ [q6, B]ZZZZZZ
   69 ⊢ Z[q6, B]ZZZZZ
   70 ⊢ ZZ[q6, B]ZZZZ
   71 ⊢ ZZZ[q6, B]ZZZ
   72 ⊢ ZZZZ[q6, B]ZZ
   73 ⊢ ZZZZZ[q6, B]Z
   74 ⊢ ZZZZZZ[q6, B]B
   75 ⊢ ZZZZZZ[qf, B]B
```

## Entrada `babbbabb`

**Resultado:** ACEPTADA — La MT se detuvo en el estado de aceptación [qf, B]  
**Pasos:** 119  
**Cinta final:** `ZZZZZZZZ`

```text
    0   [q0, B]babbbabb
    1 ⊢ y[q1, B]abbbabb
    2 ⊢ ya[q1, B]bbbabb
    3 ⊢ yab[q1, B]bbabb
    4 ⊢ yabb[q1, B]babb
    5 ⊢ yabbb[q1, B]abb
    6 ⊢ yabbba[q1, B]bb
    7 ⊢ yabbbab[q1, B]b
    8 ⊢ yabbbabb[q1, B]B
    9 ⊢ yabbbab[q2, B]b
   10 ⊢ yabbba[q3, B]by
   11 ⊢ yabbb[q3, B]aby
   12 ⊢ yabb[q3, B]baby
   13 ⊢ yab[q3, B]bbaby
   14 ⊢ ya[q3, B]bbbaby
   15 ⊢ y[q3, B]abbbaby
   16 ⊢ [q3, B]yabbbaby
   17 ⊢ y[q0, B]abbbaby
   18 ⊢ yx[q1, B]bbbaby
   19 ⊢ yxb[q1, B]bbaby
   20 ⊢ yxbb[q1, B]baby
   21 ⊢ yxbbb[q1, B]aby
   22 ⊢ yxbbba[q1, B]by
   23 ⊢ yxbbbab[q1, B]y
   24 ⊢ yxbbba[q2, B]by
   25 ⊢ yxbbb[q3, B]ayy
   26 ⊢ yxbb[q3, B]bayy
   27 ⊢ yxb[q3, B]bbayy
   28 ⊢ yx[q3, B]bbbayy
   29 ⊢ y[q3, B]xbbbayy
   30 ⊢ yx[q0, B]bbbayy
   31 ⊢ yxy[q1, B]bbayy
   32 ⊢ yxyb[q1, B]bayy
   33 ⊢ yxybb[q1, B]ayy
   34 ⊢ yxybba[q1, B]yy
   35 ⊢ yxybb[q2, B]ayy
   36 ⊢ yxyb[q3, B]bxyy
   37 ⊢ yxy[q3, B]bbxyy
   38 ⊢ yx[q3, B]ybbxyy
   39 ⊢ yxy[q0, B]bbxyy
   40 ⊢ yxyy[q1, B]bxyy
   41 ⊢ yxyyb[q1, B]xyy
   42 ⊢ yxyy[q2, B]bxyy
   43 ⊢ yxy[q3, B]yyxyy
   44 ⊢ yxyy[q0, B]yxyy
   45 ⊢ yxyyb[q4, B]xyy
   46 ⊢ yxyyba[q4, B]yy
   47 ⊢ yxyybab[q4, B]y
   48 ⊢ yxyybabb[q4, B]B
   49 ⊢ yxyybab[q5, B]b
   50 ⊢ yxyyba[q5, B]bb
   51 ⊢ yxyyb[q5, B]abb
   52 ⊢ yxyy[q5, B]babb
   53 ⊢ yxy[q5, B]ybabb
   54 ⊢ yx[q5, B]yybabb
   55 ⊢ y[q5, B]xyybabb
   56 ⊢ [q5, B]yxyybabb
   57 ⊢ [q5, B]Byxyybabb
   58 ⊢ [q6, B]yxyybabb
   59 ⊢ Z[q7, b]xyybabb
   60 ⊢ Zx[q7, b]yybabb
   61 ⊢ Zxy[q7, b]ybabb
   62 ⊢ Zxyy[q7, b]babb
   63 ⊢ Zxy[q8, B]yZabb
   64 ⊢ Zx[q8, B]yyZabb
   65 ⊢ Z[q8, B]xyyZabb
   66 ⊢ [q8, B]ZxyyZabb
   67 ⊢ [q8, B]BZxyyZabb
   68 ⊢ [q6, B]ZxyyZabb
   69 ⊢ Z[q6, B]xyyZabb
   70 ⊢ ZZ[q7, a]yyZabb
   71 ⊢ ZZy[q7, a]yZabb
   72 ⊢ ZZyy[q7, a]Zabb
   73 ⊢ ZZyyZ[q7, a]abb
   74 ⊢ ZZyy[q8, B]ZZbb
   75 ⊢ ZZy[q8, B]yZZbb
   76 ⊢ ZZ[q8, B]yyZZbb
   77 ⊢ Z[q8, B]ZyyZZbb
   78 ⊢ [q8, B]ZZyyZZbb
   79 ⊢ [q8, B]BZZyyZZbb
   80 ⊢ [q6, B]ZZyyZZbb
   81 ⊢ Z[q6, B]ZyyZZbb
   82 ⊢ ZZ[q6, B]yyZZbb
   83 ⊢ ZZZ[q7, b]yZZbb
   84 ⊢ ZZZy[q7, b]ZZbb
   85 ⊢ ZZZyZ[q7, b]Zbb
   86 ⊢ ZZZyZZ[q7, b]bb
   87 ⊢ ZZZyZ[q8, B]ZZb
   88 ⊢ ZZZy[q8, B]ZZZb
   89 ⊢ ZZZ[q8, B]yZZZb
   90 ⊢ ZZ[q8, B]ZyZZZb
   91 ⊢ Z[q8, B]ZZyZZZb
   92 ⊢ [q8, B]ZZZyZZZb
   93 ⊢ [q8, B]BZZZyZZZb
   94 ⊢ [q6, B]ZZZyZZZb
   95 ⊢ Z[q6, B]ZZyZZZb
   96 ⊢ ZZ[q6, B]ZyZZZb
   97 ⊢ ZZZ[q6, B]yZZZb
   98 ⊢ ZZZZ[q7, b]ZZZb
   99 ⊢ ZZZZZ[q7, b]ZZb
  100 ⊢ ZZZZZZ[q7, b]Zb
  101 ⊢ ZZZZZZZ[q7, b]b
  102 ⊢ ZZZZZZ[q8, B]ZZ
  103 ⊢ ZZZZZ[q8, B]ZZZ
  104 ⊢ ZZZZ[q8, B]ZZZZ
  105 ⊢ ZZZ[q8, B]ZZZZZ
  106 ⊢ ZZ[q8, B]ZZZZZZ
  107 ⊢ Z[q8, B]ZZZZZZZ
  108 ⊢ [q8, B]ZZZZZZZZ
  109 ⊢ [q8, B]BZZZZZZZZ
  110 ⊢ [q6, B]ZZZZZZZZ
  111 ⊢ Z[q6, B]ZZZZZZZ
  112 ⊢ ZZ[q6, B]ZZZZZZ
  113 ⊢ ZZZ[q6, B]ZZZZZ
  114 ⊢ ZZZZ[q6, B]ZZZZ
  115 ⊢ ZZZZZ[q6, B]ZZZ
  116 ⊢ ZZZZZZ[q6, B]ZZ
  117 ⊢ ZZZZZZZ[q6, B]Z
  118 ⊢ ZZZZZZZZ[q6, B]B
  119 ⊢ ZZZZZZZZ[qf, B]B
```

## Entrada `aabbaabb`

**Resultado:** ACEPTADA — La MT se detuvo en el estado de aceptación [qf, B]  
**Pasos:** 119  
**Cinta final:** `ZZZZZZZZ`

```text
    0   [q0, B]aabbaabb
    1 ⊢ x[q1, B]abbaabb
    2 ⊢ xa[q1, B]bbaabb
    3 ⊢ xab[q1, B]baabb
    4 ⊢ xabb[q1, B]aabb
    5 ⊢ xabba[q1, B]abb
    6 ⊢ xabbaa[q1, B]bb
    7 ⊢ xabbaab[q1, B]b
    8 ⊢ xabbaabb[q1, B]B
    9 ⊢ xabbaab[q2, B]b
   10 ⊢ xabbaa[q3, B]by
   11 ⊢ xabba[q3, B]aby
   12 ⊢ xabb[q3, B]aaby
   13 ⊢ xab[q3, B]baaby
   14 ⊢ xa[q3, B]bbaaby
   15 ⊢ x[q3, B]abbaaby
   16 ⊢ [q3, B]xabbaaby
   17 ⊢ x[q0, B]abbaaby
   18 ⊢ xx[q1, B]bbaaby
   19 ⊢ xxb[q1, B]baaby
   20 ⊢ xxbb[q1, B]aaby
   21 ⊢ xxbba[q1, B]aby
   22 ⊢ xxbbaa[q1, B]by
   23 ⊢ xxbbaab[q1, B]y
   24 ⊢ xxbbaa[q2, B]by
   25 ⊢ xxbba[q3, B]ayy
   26 ⊢ xxbb[q3, B]aayy
   27 ⊢ xxb[q3, B]baayy
   28 ⊢ xx[q3, B]bbaayy
   29 ⊢ x[q3, B]xbbaayy
   30 ⊢ xx[q0, B]bbaayy
   31 ⊢ xxy[q1, B]baayy
   32 ⊢ xxyb[q1, B]aayy
   33 ⊢ xxyba[q1, B]ayy
   34 ⊢ xxybaa[q1, B]yy
   35 ⊢ xxyba[q2, B]ayy
   36 ⊢ xxyb[q3, B]axyy
   37 ⊢ xxy[q3, B]baxyy
   38 ⊢ xx[q3, B]ybaxyy
   39 ⊢ xxy[q0, B]baxyy
   40 ⊢ xxyy[q1, B]axyy
   41 ⊢ xxyya[q1, B]xyy
   42 ⊢ xxyy[q2, B]axyy
   43 ⊢ xxy[q3, B]yxxyy
   44 ⊢ xxyy[q0, B]xxyy
   45 ⊢ xxyya[q4, B]xyy
   46 ⊢ xxyyaa[q4, B]yy
   47 ⊢ xxyyaab[q4, B]y
   48 ⊢ xxyyaabb[q4, B]B
   49 ⊢ xxyyaab[q5, B]b
   50 ⊢ xxyyaa[q5, B]bb
   51 ⊢ xxyya[q5, B]abb
   52 ⊢ xxyy[q5, B]aabb
   53 ⊢ xxy[q5, B]yaabb
   54 ⊢ xx[q5, B]yyaabb
   55 ⊢ x[q5, B]xyyaabb
   56 ⊢ [q5, B]xxyyaabb
   57 ⊢ [q5, B]Bxxyyaabb
   58 ⊢ [q6, B]xxyyaabb
   59 ⊢ Z[q7, a]xyyaabb
   60 ⊢ Zx[q7, a]yyaabb
   61 ⊢ Zxy[q7, a]yaabb
   62 ⊢ Zxyy[q7, a]aabb
   63 ⊢ Zxy[q8, B]yZabb
   64 ⊢ Zx[q8, B]yyZabb
   65 ⊢ Z[q8, B]xyyZabb
   66 ⊢ [q8, B]ZxyyZabb
   67 ⊢ [q8, B]BZxyyZabb
   68 ⊢ [q6, B]ZxyyZabb
   69 ⊢ Z[q6, B]xyyZabb
   70 ⊢ ZZ[q7, a]yyZabb
   71 ⊢ ZZy[q7, a]yZabb
   72 ⊢ ZZyy[q7, a]Zabb
   73 ⊢ ZZyyZ[q7, a]abb
   74 ⊢ ZZyy[q8, B]ZZbb
   75 ⊢ ZZy[q8, B]yZZbb
   76 ⊢ ZZ[q8, B]yyZZbb
   77 ⊢ Z[q8, B]ZyyZZbb
   78 ⊢ [q8, B]ZZyyZZbb
   79 ⊢ [q8, B]BZZyyZZbb
   80 ⊢ [q6, B]ZZyyZZbb
   81 ⊢ Z[q6, B]ZyyZZbb
   82 ⊢ ZZ[q6, B]yyZZbb
   83 ⊢ ZZZ[q7, b]yZZbb
   84 ⊢ ZZZy[q7, b]ZZbb
   85 ⊢ ZZZyZ[q7, b]Zbb
   86 ⊢ ZZZyZZ[q7, b]bb
   87 ⊢ ZZZyZ[q8, B]ZZb
   88 ⊢ ZZZy[q8, B]ZZZb
   89 ⊢ ZZZ[q8, B]yZZZb
   90 ⊢ ZZ[q8, B]ZyZZZb
   91 ⊢ Z[q8, B]ZZyZZZb
   92 ⊢ [q8, B]ZZZyZZZb
   93 ⊢ [q8, B]BZZZyZZZb
   94 ⊢ [q6, B]ZZZyZZZb
   95 ⊢ Z[q6, B]ZZyZZZb
   96 ⊢ ZZ[q6, B]ZyZZZb
   97 ⊢ ZZZ[q6, B]yZZZb
   98 ⊢ ZZZZ[q7, b]ZZZb
   99 ⊢ ZZZZZ[q7, b]ZZb
  100 ⊢ ZZZZZZ[q7, b]Zb
  101 ⊢ ZZZZZZZ[q7, b]b
  102 ⊢ ZZZZZZ[q8, B]ZZ
  103 ⊢ ZZZZZ[q8, B]ZZZ
  104 ⊢ ZZZZ[q8, B]ZZZZ
  105 ⊢ ZZZ[q8, B]ZZZZZ
  106 ⊢ ZZ[q8, B]ZZZZZZ
  107 ⊢ Z[q8, B]ZZZZZZZ
  108 ⊢ [q8, B]ZZZZZZZZ
  109 ⊢ [q8, B]BZZZZZZZZ
  110 ⊢ [q6, B]ZZZZZZZZ
  111 ⊢ Z[q6, B]ZZZZZZZ
  112 ⊢ ZZ[q6, B]ZZZZZZ
  113 ⊢ ZZZ[q6, B]ZZZZZ
  114 ⊢ ZZZZ[q6, B]ZZZZ
  115 ⊢ ZZZZZ[q6, B]ZZZ
  116 ⊢ ZZZZZZ[q6, B]ZZ
  117 ⊢ ZZZZZZZ[q6, B]Z
  118 ⊢ ZZZZZZZZ[q6, B]B
  119 ⊢ ZZZZZZZZ[qf, B]B
```

## Entrada `abaab`

**Resultado:** RECHAZADA — No existe δ([q2, B], x); la MT se detuvo en un estado de no aceptación  
**Pasos:** 20  
**Cinta final:** `xyxxy`

```text
    0   [q0, B]abaab
    1 ⊢ x[q1, B]baab
    2 ⊢ xb[q1, B]aab
    3 ⊢ xba[q1, B]ab
    4 ⊢ xbaa[q1, B]b
    5 ⊢ xbaab[q1, B]B
    6 ⊢ xbaa[q2, B]b
    7 ⊢ xba[q3, B]ay
    8 ⊢ xb[q3, B]aay
    9 ⊢ x[q3, B]baay
   10 ⊢ [q3, B]xbaay
   11 ⊢ x[q0, B]baay
   12 ⊢ xy[q1, B]aay
   13 ⊢ xya[q1, B]ay
   14 ⊢ xyaa[q1, B]y
   15 ⊢ xya[q2, B]ay
   16 ⊢ xy[q3, B]axy
   17 ⊢ x[q3, B]yaxy
   18 ⊢ xy[q0, B]axy
   19 ⊢ xyx[q1, B]xy
   20 ⊢ xy[q2, B]xxy
```

## Entrada `abbaab`

**Resultado:** RECHAZADA — No existe δ([q7, b], a); la MT se detuvo en un estado de no aceptación  
**Pasos:** 50  
**Cinta final:** `ZZyZab`

```text
    0   [q0, B]abbaab
    1 ⊢ x[q1, B]bbaab
    2 ⊢ xb[q1, B]baab
    3 ⊢ xbb[q1, B]aab
    4 ⊢ xbba[q1, B]ab
    5 ⊢ xbbaa[q1, B]b
    6 ⊢ xbbaab[q1, B]B
    7 ⊢ xbbaa[q2, B]b
    8 ⊢ xbba[q3, B]ay
    9 ⊢ xbb[q3, B]aay
   10 ⊢ xb[q3, B]baay
   11 ⊢ x[q3, B]bbaay
   12 ⊢ [q3, B]xbbaay
   13 ⊢ x[q0, B]bbaay
   14 ⊢ xy[q1, B]baay
   15 ⊢ xyb[q1, B]aay
   16 ⊢ xyba[q1, B]ay
   17 ⊢ xybaa[q1, B]y
   18 ⊢ xyba[q2, B]ay
   19 ⊢ xyb[q3, B]axy
   20 ⊢ xy[q3, B]baxy
   21 ⊢ x[q3, B]ybaxy
   22 ⊢ xy[q0, B]baxy
   23 ⊢ xyy[q1, B]axy
   24 ⊢ xyya[q1, B]xy
   25 ⊢ xyy[q2, B]axy
   26 ⊢ xy[q3, B]yxxy
   27 ⊢ xyy[q0, B]xxy
   28 ⊢ xyya[q4, B]xy
   29 ⊢ xyyaa[q4, B]y
   30 ⊢ xyyaab[q4, B]B
   31 ⊢ xyyaa[q5, B]b
   32 ⊢ xyya[q5, B]ab
   33 ⊢ xyy[q5, B]aab
   34 ⊢ xy[q5, B]yaab
   35 ⊢ x[q5, B]yyaab
   36 ⊢ [q5, B]xyyaab
   37 ⊢ [q5, B]Bxyyaab
   38 ⊢ [q6, B]xyyaab
   39 ⊢ Z[q7, a]yyaab
   40 ⊢ Zy[q7, a]yaab
   41 ⊢ Zyy[q7, a]aab
   42 ⊢ Zy[q8, B]yZab
   43 ⊢ Z[q8, B]yyZab
   44 ⊢ [q8, B]ZyyZab
   45 ⊢ [q8, B]BZyyZab
   46 ⊢ [q6, B]ZyyZab
   47 ⊢ Z[q6, B]yyZab
   48 ⊢ ZZ[q7, b]yZab
   49 ⊢ ZZy[q7, b]Zab
   50 ⊢ ZZyZ[q7, b]ab
```

## Entrada `aabbab`

**Resultado:** RECHAZADA — No existe δ([q7, a], b); la MT se detuvo en un estado de no aceptación  
**Pasos:** 41  
**Cinta final:** `Zxybab`

```text
    0   [q0, B]aabbab
    1 ⊢ x[q1, B]abbab
    2 ⊢ xa[q1, B]bbab
    3 ⊢ xab[q1, B]bab
    4 ⊢ xabb[q1, B]ab
    5 ⊢ xabba[q1, B]b
    6 ⊢ xabbab[q1, B]B
    7 ⊢ xabba[q2, B]b
    8 ⊢ xabb[q3, B]ay
    9 ⊢ xab[q3, B]bay
   10 ⊢ xa[q3, B]bbay
   11 ⊢ x[q3, B]abbay
   12 ⊢ [q3, B]xabbay
   13 ⊢ x[q0, B]abbay
   14 ⊢ xx[q1, B]bbay
   15 ⊢ xxb[q1, B]bay
   16 ⊢ xxbb[q1, B]ay
   17 ⊢ xxbba[q1, B]y
   18 ⊢ xxbb[q2, B]ay
   19 ⊢ xxb[q3, B]bxy
   20 ⊢ xx[q3, B]bbxy
   21 ⊢ x[q3, B]xbbxy
   22 ⊢ xx[q0, B]bbxy
   23 ⊢ xxy[q1, B]bxy
   24 ⊢ xxyb[q1, B]xy
   25 ⊢ xxy[q2, B]bxy
   26 ⊢ xx[q3, B]yyxy
   27 ⊢ xxy[q0, B]yxy
   28 ⊢ xxyb[q4, B]xy
   29 ⊢ xxyba[q4, B]y
   30 ⊢ xxybab[q4, B]B
   31 ⊢ xxyba[q5, B]b
   32 ⊢ xxyb[q5, B]ab
   33 ⊢ xxy[q5, B]bab
   34 ⊢ xx[q5, B]ybab
   35 ⊢ x[q5, B]xybab
   36 ⊢ [q5, B]xxybab
   37 ⊢ [q5, B]Bxxybab
   38 ⊢ [q6, B]xxybab
   39 ⊢ Z[q7, a]xybab
   40 ⊢ Zx[q7, a]ybab
   41 ⊢ Zxy[q7, a]bab
```
