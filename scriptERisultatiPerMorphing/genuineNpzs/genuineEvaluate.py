import pickle
from pathlib import Path
import numpy as np
from sklearn.svm import SVC
import csv

def merge(doc_feats: np.ndarray, live_feats: np.ndarray) -> np.ndarray:
    return doc_feats - live_feats

script_dir = Path(__file__).parent.resolve()
default_model_path = script_dir / "initial_model.pkl"
output_file = script_dir / "genuineScores.txt"

with open(default_model_path, "rb") as f:
    model_with_threshold = pickle.load(f)
    model: SVC = model_with_threshold["model"]
    print(f"Model loaded from {default_model_path.name}")

if not output_file.exists():
    with open(output_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID_SOGGETTO", "SEQUENZA", "POSA", "FRAME", "SCORE"])

for npz_file in sorted(script_dir.glob("*.npz")):
    print(f"\nProcessing file: {npz_file.name}")
    try:
        parts = npz_file.stem.split("-")
        if len(parts) != 4:
            print(f"Skipping invalid filename format: {npz_file.name}")
            continue
        id_soggetto, sequenza, posa, frame = parts

        embeds = np.load(npz_file, allow_pickle=True)
        doc_feats = embeds["doc_features"].reshape(1, -1)
        live_feats = embeds["live_features"].reshape(1, -1)
        test_x = merge(doc_feats, live_feats)

        scores = model.predict_proba(test_x)[:, 1]

        with open(output_file, mode="a", newline="") as f:
            writer = csv.writer(f)
            for score in scores:
                writer.writerow([id_soggetto, sequenza, posa, frame, f"{score:.6f}"])

        print(f"{len(scores)} scores written for {npz_file.name}")

    except Exception as e:
        print(f"Error processing {npz_file.name}: {e}")
