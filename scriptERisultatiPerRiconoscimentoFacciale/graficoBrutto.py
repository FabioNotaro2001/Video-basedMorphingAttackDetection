#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media dei punteggi 'frontal_gaze' in funzione della distanza sintetica.

• 0–700 px: contribuiscono le sequenze 01 e 02
• 700–800 px: contribuiscono solo le sequenze 02
L'asse Y è forzato a 0–100 per una scala fissa, indipendentemente
dal range effettivo dei punteggi.

File di input: CSV/txt con header:
    ID_SOGGETTO,SEQUENZA,POSA,FRAME,DISTANZA_COSENO
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Union


def plot_frontal_gaze_mean_unique(
        txt_path: Union[str, Path],
        step: int = 1,
        show_individual: bool = False) -> None:
    """Disegna la curva media dei punteggi frontal_gaze.

    Parameters
    ----------
    txt_path : Union[str, Path]
        Percorso del file di testo (CSV con virgola e header).
    step : int, default 1
        Risoluzione della griglia X (px).
    show_individual : bool, default False
        Se True mostra anche le singole curve in trasparenza.
    """
    # 1. Lettura e filtro -----------------------------------------------------
    df = pd.read_csv(txt_path)

    # Mantieni solo la posa d'interesse
    df = df[df["POSA"].str.strip() == "looking_around"].copy()

    # Formattazioni/cast
    df["SEQUENZA"] = df["SEQUENZA"].astype(str).str.zfill(2)
    df["DISTANZA_COSENO"] = df["DISTANZA_COSENO"].astype(float)

    # 2. Costruzione delle curve individuali ----------------------------------
    curves = []  # lista di tuple (x, y)

    for (_, seq, _), grp in df.groupby(["ID_SOGGETTO", "SEQUENZA", "POSA"]):
        limit = 700 if seq == "01" else 850          # X‑max per il gruppo
        n = len(grp)
        x = np.linspace(0, limit, n, endpoint=False) # ascisse equispaziate
        y = grp.sort_values("FRAME")["DISTANZA_COSENO"].to_numpy()
        curves.append((x, y))

    if not curves:
        raise ValueError("Nessuna riga con POSA = 'frontal_gaze' trovata.")

    # 3. Interpolazione su griglia 0–800 e media ------------------------------
    grid = np.arange(0, 850, step)
    stack = []

    for x, y in curves:
        # Fuori dal proprio intervallo → NaN (così non pesa nella media)
        y_interp = np.interp(grid, x, y, left=np.nan, right=np.nan)
        stack.append(y_interp)

        if show_individual:
            plt.plot(grid, y_interp, alpha=0.25, linewidth=0.8)

    stack = np.vstack(stack)
    mean_curve = np.nanmean(stack, axis=0)

    # 4. Plot -----------------------------------------------------------------
    plt.figure(figsize=(10, 5))
    plt.plot(grid, mean_curve, linewidth=2.5, label="AVG global curve")

    plt.xlabel("DISTANCE(cm)")
    plt.ylabel("SCORE")
    plt.title('AVG OF LOOKING_AROUND SCORES')
    plt.xlim(0, 850)
    plt.ylim(0, 1)            # <<— asse Y fisso 0‑100
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Cambia 'genuineScores.txt' con il percorso del tuo file
    plot_frontal_gaze_mean_unique("genuineScores.txt",
                                  step=1,
                                  show_individual=False)
