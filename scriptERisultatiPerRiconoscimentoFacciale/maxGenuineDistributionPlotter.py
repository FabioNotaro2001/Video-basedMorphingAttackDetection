import csv
import matplotlib.pyplot as plt
from collections import defaultdict

file_path = 'genuineScores.txt'

dati_raggruppati = defaultdict(list)

# Leggi il file e raggruppa per tripla
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        id_soggetto, sequenza, posa, frame, score = row
        key = (id_soggetto, sequenza, posa)
        dati_raggruppati[key].append(float(score))

punti = []

# Calcola distanza del punteggio massimo per ogni gruppo
for key, scores in dati_raggruppati.items():
    sequenza = key[1]
    num_scores = len(scores)
    distanza_max = 700 if sequenza == '01' else 850
    passo = distanza_max / num_scores
    x_vals = [distanza_max - i * passo for i in range(num_scores)]
    max_score = max(scores)
    idx_max = scores.index(max_score)
    distanza_score_max = x_vals[idx_max]
    punti.append((distanza_score_max, max_score))

x_punti, score_punti = zip(*punti)

# Grafico su una singola retta
plt.figure(figsize=(12, 2))
plt.scatter(x_punti, [0]*len(x_punti), c=score_punti, cmap='viridis', alpha=0.7, edgecolors='k')
plt.xlabel('DISTANCE (cm)')
plt.yticks([])  # Rimuove l'asse Y
plt.title('MAX SCORE DISTRIBUTION WITH RESPECT TO DISTANCE')
plt.xlim(0, 850)
plt.grid(axis='x')
plt.tight_layout()

# Salva e mostra il grafico
plt.savefig('retta_score_massimi.png')
plt.show()

print("Grafico su retta salvato come 'retta_score_massimi.png'.")
