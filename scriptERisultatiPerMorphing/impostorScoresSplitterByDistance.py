#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dividi impostorScores.txt in tre file
(long, medium, short) mantenendo l’intestazione
e suddividendo ogni gruppo (prime 5 colonne)
in tre terzi ordinati come compaiono nel file originale.
"""

import csv
from collections import defaultdict
from pathlib import Path

# --- File in ingresso/uscita ------------------------------------------------
IN_FILE  = Path("impostorScores.txt")

OUT_FILES = {
    "long":   Path("longDistanceImpostorScores.txt"),
    "medium": Path("mediumDistanceImpostorScores.txt"),
    "short":  Path("shortDistanceImpostorScores.txt"),
}

# --- Lettura dell’intero file e raggruppamento per chiave -------------------
groups = defaultdict(list)  # chiave: tuple delle prime 5 colonne -> righe

with IN_FILE.open(newline="", encoding="utf-8") as f_in:
    reader = csv.reader(f_in)
    header = next(reader)            # salva la riga di intestazione
    for row in reader:               # per ogni riga del file
        key = tuple(row[:5])         # prime 5 colonne come chiave del gruppo
        groups[key].append(row)      # conserva la riga nell’ordine d’origine

# --- Preparazione dei file di output con la stessa intestazione -------------
writers, handles = {}, {}
for label, path in OUT_FILES.items():
    handle = path.open("w", newline="", encoding="utf-8")
    writer = csv.writer(handle)
    writer.writerow(header)          # scrive subito l’intestazione
    writers[label], handles[label] = writer, handle

# --- Suddivisione di ciascun gruppo in terzi --------------------------------
for rows in groups.values():
    n = len(rows)
    x = n // 3                       # terzo intero inferiore
    # Indici di taglio: 0..x-1 (long), x..2x-1 (medium), il resto (short)
    long_part   = rows[:x]
    medium_part = rows[x:2*x]
    short_part  = rows[2*x:]         # include anche le eventuali righe in più

    for r in long_part:
        writers["long"].writerow(r)
    for r in medium_part:
        writers["medium"].writerow(r)
    for r in short_part:
        writers["short"].writerow(r)

# --- Chiusura dei file ------------------------------------------------------
for h in handles.values():
    h.close()

print("Fatto!  Generati:")
for label, path in OUT_FILES.items():
    print(f"  • {path}  ({label})")
