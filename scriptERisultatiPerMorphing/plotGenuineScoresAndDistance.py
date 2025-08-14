import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# Imposta il percorso al tuo file
file_path = 'genuineScores.txt'  # Sostituisci con il nome del tuo file

# Dizionario per raggruppare le triplette
dati_raggruppati = defaultdict(list)

# Legge il file e raggruppa per tripla
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Salta l'intestazione
    for row in reader:
        id_soggetto, sequenza, posa, frame, score = row
        key = (id_soggetto, sequenza, posa)
        dati_raggruppati[key].append(float(score))

# Crea directory per salvare i grafici se non esiste
os.makedirs('grafici', exist_ok=True)

# Genera e salva i grafici
for key, scores in dati_raggruppati.items():
    id_soggetto, sequenza, posa = key
    num_scores = len(scores)
    
    # Determina la distanza massima
    distanza_max = 700 if sequenza == '01' else 850
    
    # Calcola le distanze x in ordine inverso
    passo = distanza_max / num_scores
    x_vals = [distanza_max - i * passo for i in range(num_scores)]
    
    # Prepara il grafico
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, scores, marker='o', linestyle='-')
    plt.ylim(0, 1)
    plt.xlim(0, distanza_max)
    plt.xlabel('DISTANCE (cm)')
    plt.ylabel('SCORE (cosine distance)')
    plt.title(f'{id_soggetto}, {sequenza}, {posa}')
    plt.grid(True)
    
    # Salva l'immagine
    filename = f"grafici/{id_soggetto},{sequenza},{posa}.png"
    plt.savefig(filename)
    plt.close()

print("Grafici salvati con successo.")
