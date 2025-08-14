import numpy as np
import matplotlib.pyplot as plt

def read_and_extract_values(file_path: str) -> np.ndarray:
    # Leggi il file, ignorando la prima riga di intestazione
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # Ignora la prima riga

    # Estrai la terzultima colonna da ogni riga
    values = []
    for line in lines:
        # Dividi la riga in colonne usando il separatore ";"
        columns = line.strip().split(';')
        
        # Aggiungi il valore della terzultima colonna alla lista
        if len(columns) >= 3:  # Verifica che ci siano almeno 3 colonne
            values.append(columns[-3])  # Terzultima colonna
    
    # Converti la lista in un array numpy
    same = np.array(values, dtype=float)  # Supponendo che i valori siano numerici
    return same

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

# Specifica il percorso dei due file
file_path_1 = 'aggregatedGenuineScores.txt'
file_path_2 = 'aggregatedImpostorScores.txt'

# Leggi i valori dai due file e salvali nei vettori numpy
same = read_and_extract_values(file_path_1)
different = read_and_extract_values(file_path_2)

# Creazione di predictions (concatenazione di same e different)
predictions = np.concatenate((same, different))

# Creazione di expected, con 1 per gli elementi in same e 0 per gli elementi in different
expected = np.concatenate((np.ones(len(same)), np.zeros(len(different))))

# Stampa i risultati
print("Vettore 'same' (dal primo file):")
print(same)

print("\nVettore 'different' (dal secondo file):")
print(different)

print("\nVettore 'predictions' (concatenazione di 'same' e 'different'):")
print(predictions)

print("\nVettore 'expected' (1 per 'same' e 0 per 'different'):")
print(expected)

# Calcolare la curva ROC
Pfa, Pmiss = compute_roc(predictions, expected)
print("\nCurva ROC (False Positive Rate vs Miss Rate):")
print("False Positive Rate (Pfa):", Pfa)
print("Miss Rate (Pmiss):", Pmiss)

# Calcolare le metriche (EER e BPCER)
thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
eer, bpcer = compute_metrics(predictions, expected, thresholds)

print("\nEqual Error Rate (EER):", eer)
print("BPCER (Binary Classification Error Rate) per i threshold dati:", bpcer)

# Visualizzare la curva ROC usando Matplotlib
# Visualizzare e salvare la curva ROC usando Matplotlib
plt.figure(figsize=(8, 6))
plt.plot(Pfa, Pmiss, color='b', label='DET Curve')
plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')  # Linea diagonale (caso casuale)
plt.title('DET CURVE RELATED TO AVG SCORES')
plt.xlabel('False Positive Rate (Pfa)')
plt.ylabel('Miss Rate (Pmiss)')
plt.legend(loc='best')
plt.grid(True)

# Salva l'immagine nella stessa cartella con nome 'roc_curve.png'
plt.savefig('roc_curve.png', dpi=300, bbox_inches='tight')

# Mostra il grafico
plt.show()
