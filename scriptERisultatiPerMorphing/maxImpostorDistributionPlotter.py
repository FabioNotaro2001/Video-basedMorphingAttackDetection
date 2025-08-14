import matplotlib.pyplot as plt
import os
from collections import defaultdict

# === CONFIG ===
file_path = 'impostorScores.txt'  # <-- Percorso del file aggiornato
output_image = 'retta_score_massimi_impostor.png'

# === LETTURA FILE E RAGGRUPPAMENTO ===
gruppi = defaultdict(list)

with open(file_path, 'r', encoding='utf-8') as f:
    next(f)  # salta intestazione
    for line in f:
        parts = line.strip().split(',')
        if len(parts) != 7:
            continue
        soggetto1, soggetto2, id_frame, sequenza, posa, frame, score = parts
        key = (soggetto1, soggetto2, id_frame, sequenza, posa)
        try:
            score = float(score)
            gruppi[key].append(score)
        except ValueError:
            continue

# === CALCOLO PUNTI SCORE MASSIMI ===
punti = []

for key, scores in gruppi.items():
    sequenza = key[3]  # 4ª colonna = SEQUENZA
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

    max_score = max(scores)
    idx_max = scores.index(max_score)
    distanza_score_max = x_vals[idx_max]

    punti.append((distanza_score_max, max_score))

# === GRAFICO SU RETTA ===
if punti:
    x_punti, score_punti = zip(*punti)

    plt.figure(figsize=(12, 2))
    plt.scatter(x_punti, [0]*len(x_punti), c=score_punti, cmap='plasma', alpha=0.7, edgecolors='k')
    plt.xlabel('DISTANCE (cm)')
    plt.yticks([])  # Nasconde l'asse Y
    plt.title('MAX SCORE DISTRIBUTION WITH RESPECT TO DISTANCE')
    plt.xlim(0, 850)
    plt.grid(axis='x')
    plt.tight_layout()
    plt.savefig(output_image)
    plt.show()

    print(f"Grafico a retta salvato come '{output_image}'")
else:
    print("Nessun dato disponibile per il grafico.")
