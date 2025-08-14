import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List  # <‑‑ import per i type hints compatibili

def read_and_extract_values(file_path: str) -> np.ndarray:
    """Legge il file CSV/‑separato e restituisce l’ultima colonna come array float."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()[1:]           # salta l’intestazione

    values = []
    for line in lines:
        columns = line.strip().split(";")
        if len(columns) >= 1:
            values.append(columns[-2])         # ultima colonna (se era effettivamente quella d’interesse)

    return np.asarray(values, dtype=float)

def compute_roc(y_pred: np.ndarray, y_true: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Restituisce Pfa e Pmiss (False Positive Rate, Miss Rate)."""
    y_pred_n = 1 - y_pred
    y_true_n = 1 - y_true

    num_preds       = y_pred.shape[0]
    num_positives   = np.count_nonzero(y_true_n)
    num_negatives   = num_preds - num_positives

    if num_positives == 0:
        raise ValueError("No positive samples in y_true")
    if num_negatives == 0:
        raise ValueError("No negative samples in y_true")

    predicted_positives = np.arange(1, num_preds + 1)
    sorted_true  = np.argsort(-y_true_n, kind="stable")
    sorted_pred  = np.argsort(y_pred_n[sorted_true], kind="stable")

    false_positives = np.cumsum(y_true_n[sorted_true][sorted_pred])
    false_negatives = num_negatives - (predicted_positives - false_positives)

    Pfa   = np.empty(num_preds + 1, dtype=float)
    Pmiss = np.empty(num_preds + 1, dtype=float)

    Pfa[0]   = 1.0
    Pmiss[0] = 0.0
    Pfa[1:]   = false_negatives / num_negatives
    Pmiss[1:] = false_positives / num_positives
    return Pfa, Pmiss

def compute_metrics(y_pred: np.ndarray, y_true: np.ndarray,
                    thresholds: List[float]) -> Tuple[float, np.ndarray]:
    """Calcola EER e BPCER per i threshold forniti."""
    Pfa, Pmiss = compute_roc(y_pred, y_true)

    eer_idx = np.nonzero(Pfa <= Pmiss)[0][0]
    eer     = (Pmiss[eer_idx - 1] + Pfa[eer_idx]) / 2

    np_thr  = np.asarray(thresholds, dtype=np.float32)
    bpcer_idx = Pfa.size - 1 - np.searchsorted(Pfa[::-1], np_thr, side="right")

    d1 = np.abs(np_thr - Pmiss[bpcer_idx - 1])
    d2 = np.abs(np_thr - Pmiss[bpcer_idx])
    w1 = d1 / (d1 + d2)
    w2 = d2 / (d1 + d2)

    bpcer = np.where(Pmiss[bpcer_idx - 1] == Pmiss[bpcer_idx],
                     Pmiss[bpcer_idx],
                     Pmiss[bpcer_idx - 1] * w1 + Pmiss[bpcer_idx] * w2)
    return eer, bpcer

# --- Percorsi ai file ---------------------------------------------------------
file_path_1 = "aggregatedGenuineScores.txt"
file_path_2 = "aggregatedImpostorScores.txt"

# --- Lettura dei dati ---------------------------------------------------------
same      = read_and_extract_values(file_path_1)
different = read_and_extract_values(file_path_2)

# Predizioni e ground‑truth
predictions = np.concatenate((same, different))
expected    = np.concatenate((np.ones_like(same), np.zeros_like(different)))

# --- Curva ROC e metriche -----------------------------------------------------
Pfa, Pmiss = compute_roc(predictions, expected)
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
eer, bpcer = compute_metrics(predictions, expected, thresholds)

print(f"EER: {eer:.4f}")
print(f"BPCER: {bpcer}")

# --- Visualizzazione: ISTOGRAMMI ---------------------------------------------
plt.figure(figsize=(10, 5))

plt.hist(same,      bins=30, alpha=0.6, color="blue",  label="Genuine",  edgecolor="black")
plt.hist(different, bins=30, alpha=0.6, color="red",   label="Impostor", edgecolor="black")

plt.title("Scores Distribution: Genuine vs Impostor")
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.grid(True)
plt.legend(loc="upper right")

plt.tight_layout()
plt.savefig("score_distribution_histogram.png", dpi=300)
plt.show()
