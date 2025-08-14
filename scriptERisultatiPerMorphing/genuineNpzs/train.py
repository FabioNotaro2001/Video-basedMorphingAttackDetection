import argparse
from pathlib import Path
import pickle

import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import roc_curve


def merge(doc_feats: np.ndarray, live_feats: np.ndarray) -> np.ndarray:
    return doc_feats - live_feats


parser = argparse.ArgumentParser()
parser.add_argument("--train-embeds", type=Path, required=True)
parser.add_argument("--test-embeds", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()

train_embeds = np.load(args.train_embeds, allow_pickle=True)
train_x = merge(train_embeds["doc_features"], train_embeds["live_features"])
train_y = np.where(train_embeds["cls"] != 0, 1, 0)

test_embeds = np.load(args.test_embeds, allow_pickle=True)
test_x = merge(test_embeds["doc_features"], test_embeds["live_features"])
test_y = np.where(test_embeds["cls"] != 0, 1, 0)

print(f"Train shape: {train_x.shape}, {train_y.shape}")
print(f"Test shape: {test_x.shape}, {test_y.shape}")
print(f"Positive training samples: {np.count_nonzero(train_y)}, negative training samples: {train_y.shape[0] - np.count_nonzero(train_y)}")
print(f"Positive testing samples: {np.count_nonzero(test_y)}, negative testing samples: {test_y.shape[0] - np.count_nonzero(test_y)}")

model = SVC(probability=True, verbose=True)
model.fit(train_x, train_y)
test_y_pred = model.predict_proba(test_x)[:, 1]

# Export scores divided by ground truth
np.savetxt("y_pred_from_train.txt", test_y_pred)
np.savetxt("y_true_from_train.txt", test_y)

fpr, tpr, thresholds = roc_curve(test_y, test_y_pred)
# Compute EER – i.e. the error where APCER (false negative rate on morphs) equals BPCER (false positive rate on bona fide)
fnr = 1 - tpr  # false negative rate on attack (morphed) samples; APCER in this context
abs_diffs = np.abs(fpr - fnr)
eer_index = np.nanargmin(abs_diffs)
eer_threshold = thresholds[eer_index]
eer = (fpr[eer_index] + fnr[eer_index]) / 2  # average error at this threshold

print(f"EER: {eer:.4f} at score threshold: {eer_threshold:.4f}")

# Define target APCER values.
# Note: APCER is the proportion of morphs misclassified as bona fide.
# roc_curve returns thresholds in descending order. At high thresholds, few samples are called positive,
# so tpr (and 1-tpr) is low/high respectively. As the threshold decreases, tpr increases and therefore APCER (1-tpr) decreases.
target_apcer = [0.1, 0.05, 0.01]
found_thresholds = []

for target in target_apcer:
    # Find the threshold where the false negative rate (APCER) is as close as possible to the target
    idx = np.argmin(np.abs(fnr - target))
    threshold_target = thresholds[idx]
    found_thresholds.append(threshold_target)
    achieved_apcer = fnr[idx]
    bpcer = fpr[idx]  # BPCER: bona fide samples misclassified as morphed
    print(f"For target APCER = {target:.2f}: "
          f"threshold = {threshold_target:.4f}, achieved APCER = {achieved_apcer:.4f}, "
          f"BPCER = {bpcer:.4f}")

with open(args.output, "wb") as f:
    model_with_thresholds = {
        "model": model,
        "threshold": [eer_threshold] + found_thresholds,
    }
    pickle.dump(model_with_thresholds, f)