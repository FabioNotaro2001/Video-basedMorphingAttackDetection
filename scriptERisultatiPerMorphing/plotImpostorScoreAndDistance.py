import matplotlib.pyplot as plt
import os
from collections import defaultdict

# === CONFIG ===
file_path = 'impostorScores.txt'  # <-- Percorso del nuovo file CSV
output_dir = 'graficiImpostor'
os.makedirs(output_dir, exist_ok=True)

# === LETTURA FILE E RAGGRUPPAMENTO ===
gruppi = defaultdict(list)

with open(file_path, 'r', encoding='utf-8') as f:
    next(f)  # salta intestazione
    for line in f:
        parts = line.strip().split(',')
        if len(parts) != 7:
            continue  # skip righe malformate
        id1, id2, frame_id, sequenza, posa, frame, score = parts
        key = (id1, id2, frame_id, sequenza, posa)
        try:
            score = float(score)
            gruppi[key].append(score)
        except ValueError:
            continue  # salta se non riesce a convertire il valore in float

# === GENERAZIONE GRAFICI ===
for key, scores in gruppi.items():
    id1, id2, frame_id, sequenza, posa = key

    if sequenza == '01':
        distanza_totale = 700
    elif sequenza == '02':
        distanza_totale = 850
    else:
        print(f"Sequenza sconosciuta: {sequenza} – salto")
        continue

    n = len(scores)
    if n == 0:
        continue

    passo = distanza_totale / n
    x_vals = [distanza_totale - i * passo for i in range(n)]
    y_vals = scores

    try:
        # Creazione grafico
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x_vals, y_vals, marker='o', linestyle='-', color='blue')
        ax.set_ylim(0, 1)
        ax.set_xlabel('DISTANCE (cm)')
        ax.set_ylabel('SCORE (cosine distance)')
        ax.set_title(f'{id1};{id2};{frame_id};{sequenza};{posa}')
        ax.grid(True)

        # Salvataggio grafico
        nome_file = f'{id1};{id2};{frame_id};{sequenza};{posa}.png'
        nome_file = nome_file.replace("/", "_").replace("\\", "_")
        fig.savefig(os.path.join(output_dir, nome_file))
        plt.close(fig)
    except Exception as e:
        print(f"Errore nella generazione del grafico per {key}: {e}")
