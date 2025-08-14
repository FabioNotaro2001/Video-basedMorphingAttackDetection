import numpy as np
import matplotlib.pyplot as plt

def read_and_extract_values(file_path: str, separator: str) -> np.ndarray:
    # Leggi il file ignorando la prima riga (intestazione)
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Salta l'intestazione

    values = []
    for line in lines:
        columns = line.strip().split(separator)
        if len(columns) >= 3:
            values.append(columns[-1])  # Terzultima colonna

    return np.array(values, dtype=float)

def compute_roc(y_pred: np.ndarray, y_true: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
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
    false_positives = np.cumsum(y_true_n[sorted_true][sorted_pred], axis=0)
    false_negatives = num_negatives - (predicted_positives - false_positives)
    Pfa = np.zeros(num_preds + 1)
    Pmiss = np.zeros(num_preds + 1)
    Pfa[0] = 1
    Pmiss[0] = 0
    Pfa[1:] = false_negatives / num_negatives
    Pmiss[1:] = false_positives / num_positives
    return Pfa, Pmiss

def compute_metrics(y_pred: np.ndarray, y_true: np.ndarray, thresholds: list[float]) -> tuple[float, np.ndarray]:
    Pfa, Pmiss = compute_roc(y_pred, y_true)
    eer_idx = np.nonzero(Pfa <= Pmiss)[0][0]
    eer = (Pmiss[eer_idx - 1] + Pfa[eer_idx]) / 2
    np_thresholds = np.array(thresholds, dtype=np.float32)
    bpcer_idx = Pfa.shape[0] - np.searchsorted(np.flip(Pfa, axis=0), np_thresholds, side="right")
    d1 = np.abs(np_thresholds - Pmiss[bpcer_idx - 1])
    d2 = np.abs(np_thresholds - Pmiss[bpcer_idx])
    w1 = d1 / (d1 + d2)
    w2 = d2 / (d1 + d2)
    bpcer = np.where(Pmiss[bpcer_idx - 1] == Pmiss[bpcer_idx], Pmiss[bpcer_idx], Pmiss[bpcer_idx - 1] * w1 + Pmiss[bpcer_idx] * w2)
    return eer, bpcer

# File paths
file_path_genuine = 'shortDistanceAggregatedGenuineScores.txt'
file_path_impostor = 'shortDistanceAggregatedImpostorScores.txt'

# Lettura dei punteggi
genuine_scores = read_and_extract_values(file_path_genuine, separator=',')
impostor_scores = read_and_extract_values(file_path_impostor, separator=';')

# Creazione vettori predictions e expected (etichetta invertita)
predictions = np.concatenate((genuine_scores, impostor_scores))
expected = np.concatenate((np.zeros(len(genuine_scores)), np.ones(len(impostor_scores))))

# Calcolo ROC
Pfa, Pmiss = compute_roc(predictions, expected)

# Calcolo metriche
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
eer, bpcer = compute_metrics(predictions, expected, thresholds)

# Stampa dei risultati
print("\nEqual Error Rate (EER):", eer)
print("BPCER per i threshold dati:", bpcer)

# Grafico ROC/DET
plt.figure(figsize=(8, 6))
plt.plot(Pfa, Pmiss, color='b', label='DET Curve')
plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
plt.title('DET Curve')
plt.xlabel('False Positive Rate (Pfa)')
plt.ylabel('Miss Rate (Pmiss)')
plt.legend(loc='best')
plt.grid(True)
plt.savefig('shortDistanceMinDet.png', dpi=300, bbox_inches='tight')
plt.show()
