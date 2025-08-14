import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List   # ← aggiunto

def read_and_extract_values(file_path: str, delimiter: str) -> np.ndarray:
    """Legge il file e restituisce la terzultima colonna come array di float."""
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # salta l'intestazione

    values = []
    for line in lines:
        columns = line.strip().split(delimiter)
        if len(columns) >= 3:               # serve almeno 3 colonne
            values.append(columns[-3])      # terzultima colonna
    return np.array(values, dtype=float)

def compute_roc(y_pred: np.ndarray, y_true: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    y_pred_n = 1 - y_pred
    y_true_n = 1 - y_true
    num_preds = y_pred.shape[0]
    num_positives = np.count_nonzero(y_true_n)
    num_negatives = num_preds - num_positives
    if num_positives == 0:
        raise ValueError("No positive samples in y_true")
    if num_negatives == 0:
        raise ValueError("No negative samples in y_true")

    predicted_positives = np.arange(1, num_preds + 1)
    sorted_true = np.argsort(-y_true_n, kind="stable")
    sorted_pred = np.argsort(y_pred_n[sorted_true], kind="stable")
    false_positives = np.cumsum(y_true_n[sorted_true][sorted_pred])
    false_negatives = num_negatives - (predicted_positives - false_positives)

    Pfa = np.zeros(num_preds + 1)
    Pmiss = np.zeros(num_preds + 1)
    Pfa[0] = 1
    Pmiss[0] = 0
    Pfa[1:] = false_negatives / num_negatives
    Pmiss[1:] = false_positives / num_positives
    return Pfa, Pmiss

def compute_metrics(y_pred: np.ndarray, y_true: np.ndarray, thresholds: List[float]) -> Tuple[float, np.ndarray]:
    Pfa, Pmiss = compute_roc(y_pred, y_true)
    eer_idx = np.nonzero(Pfa <= Pmiss)[0][0]
    eer = (Pmiss[eer_idx - 1] + Pfa[eer_idx]) / 2

    np_thresholds = np.array(thresholds, dtype=np.float32)
    bpcer_idx = Pfa.shape[0] - np.searchsorted(np.flip(Pfa), np_thresholds, side="right")
    d1 = np.abs(np_thresholds - Pmiss[bpcer_idx - 1])
    d2 = np.abs(np_thresholds - Pmiss[bpcer_idx])
    w1 = d1 / (d1 + d2)
    w2 = d2 / (d1 + d2)
    bpcer = np.where(
        Pmiss[bpcer_idx - 1] == Pmiss[bpcer_idx],
        Pmiss[bpcer_idx],
        Pmiss[bpcer_idx - 1] * w1 + Pmiss[bpcer_idx] * w2
    )
    return eer, bpcer

# Percorsi ai file
file_path_1 = 'aggregatedGenuineScores.txt'   # usa la virgola ","
file_path_2 = 'aggregatedImpostorScores.txt'  # usa il punto e virgola ";"

# Lettura dei valori
genuine_scores = read_and_extract_values(file_path_1, delimiter=',')
impostor_scores = read_and_extract_values(file_path_2, delimiter=';')

# Etichette: Genuine = 0, Impostor = 1
predictions = np.concatenate((genuine_scores, impostor_scores))
expected = np.concatenate((np.zeros(len(genuine_scores)), np.ones(len(impostor_scores))))

# Output di controllo
print("Genuine scores (0):", genuine_scores)
print("Impostor scores (1):", impostor_scores)
print("Predictions:", predictions)
print("Expected labels:", expected)

# ROC
Pfa, Pmiss = compute_roc(predictions, expected)
print("Pfa:", Pfa)
print("Pmiss:", Pmiss)

# Metriche
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
eer, bpcer = compute_metrics(predictions, expected, thresholds)
print("EER:", eer)
print("BPCER:", bpcer)

# Istogramma distribuzione score
plt.figure(figsize=(10, 4))
bins = np.linspace(predictions.min(), predictions.max(), 50)

plt.hist(genuine_scores, bins=bins, alpha=0.6, color='blue',
         label='Genuine (0)', edgecolor='black')
plt.hist(impostor_scores, bins=bins, alpha=0.6, color='red',
         label='Impostor (1)', edgecolor='black')

plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title('Histogram: Score Distribution based on AVG for Genuine vs Impostor')
plt.ylim(0, 100)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('score_distribution_histogram.png', dpi=300)
plt.show()
