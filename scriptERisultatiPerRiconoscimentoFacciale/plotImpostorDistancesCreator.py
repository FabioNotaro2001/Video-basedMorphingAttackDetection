import matplotlib.pyplot as plt
import os
from collections import defaultdict

# === CONFIG ===
file_path = 'impostorScores.txt'  # <-- Cambia con il percorso del tuo file .txt
output_dir = 'graficiImpostor'
os.makedirs(output_dir, exist_ok=True)

# === LETTURA FILE E RAGGRUPPAMENTO ===
gruppi = defaultdict(list)

with open(file_path, 'r', encoding='utf-8') as f:
    next(f)  # salta intestazione
    for line in f:
        parts = line.strip().split(';')
        if len(parts) != 6:
            continue  # skip righe malformate
        person_id, other_id, sequence, mode, frame_id, cosine_distance = parts
        key = (person_id, other_id, sequence, mode)
        try:
            cosine_distance = float(cosine_distance)
            gruppi[key].append(cosine_distance)
        except ValueError:
            continue  # salta se non riesce a convertire il valore in float

# === GENERAZIONE GRAFICI ===
for key, scores in gruppi.items():
    person_id, other_id, sequence, mode = key

    if sequence == '01':
        distanza_totale = 700
    elif sequence == '02':
        distanza_totale = 850
    else:
        print(f"Sequenza sconosciuta: {sequence} – salto")
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
        ax.set_title(f'{person_id};{other_id};{sequence};{mode}')
        ax.grid(True)

        # Salvataggio grafico
        nome_file = f'{person_id};{other_id};{sequence};{mode}.png'
        nome_file = nome_file.replace("/", "_").replace("\\", "_")  # per sicurezza
        fig.savefig(os.path.join(output_dir, nome_file))
        plt.close(fig)  # CHIUDI esplicitamente la figura
    except Exception as e:
        print(f"Errore nella generazione del grafico per {key}: {e}")
        plt.close('all')  # chiude tutto se qualcosa va storto

print("Grafici generati e salvati in:", output_dir)
