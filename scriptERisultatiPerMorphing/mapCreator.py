import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === 1) Lettura del file (salta l’intestazione) =============================
file_path = "impostorScores.txt"
df = pd.read_csv(file_path, header=None, skiprows=1)

df.columns = ['subject1', 'subject2', 'probe_subject',
              'col4', 'col5', 'col6', 'score']

# === 2) Identificatore del morph e conteggi =================================
df['morph_id'] = list(zip(df['subject1'], df['subject2']))
group_counts = df.groupby(['morph_id', 'probe_subject']).size()

m_min_per_morph = group_counts.groupby(level=0).min()
m_min = m_min_per_morph.min()

# Triple che realizzano il minimo
triples_min = group_counts[group_counts == m_min].index.to_list()

print(f"m_min (numero minimo di probe per soggetto su tutti i morph): {m_min}")
print("Triple che realizzano m_min:")
for (s1, s2), probe_subj in triples_min:
    print(f"  (subject1={s1}, subject2={s2}, probe_subject={probe_subj})")

# === 3) Parametri ===========================================================
threshold = 0.49320          # soglia ArcFace

# Valori di r desiderati: 1, 10, 25, 50, e multipli di 100 < m_min
r_values = [1, 10, 25, 50] + [r for r in range(100, m_min, 100)]
# Tieni solo quelli ≤ m_min, rimuovi eventuali duplicati e ordina
r_values = sorted(set(filter(lambda x: x <= m_min, r_values)))

if not r_values:
    raise ValueError("Nessun valore di r valido (controlla m_min).")

# === 4) Calcolo MAP solo per r in r_values ==================================
map_values = []
morph_groups = df.groupby('morph_id')

for r in r_values:
    valid_morphs = success_morphs = 0

    for morph_id, group in morph_groups:
        subj1, subj2 = morph_id
        scores1 = group[group['probe_subject'] == subj1]['score'].values
        scores2 = group[group['probe_subject'] == subj2]['score'].values

        if len(scores1) >= r and len(scores2) >= r:
            valid_morphs += 1

            sel1 = np.random.choice(scores1, r, replace=False)
            sel2 = np.random.choice(scores2, r, replace=False)

            if (sel1 > threshold).sum() >= r and (sel2 > threshold).sum() >= r:
                success_morphs += 1

    map_values.append(success_morphs / valid_morphs if valid_morphs else 0.0)

map_array = np.array(map_values).reshape(-1, 1)

# === 5) Visualizzazione =====================================================
plt.figure(figsize=(4, len(r_values) * 0.5 + 1))
sns.heatmap(map_array,
            annot=True, fmt=".2%",
            cmap="RdYlGn",
            yticklabels=[str(r) for r in r_values],
            xticklabels=["ArcFace"],
            cbar=False)            # ← niente barra laterale

plt.title("Morphing Attack Potential (MAP) on long distances")
plt.ylabel("Verification attempts (r)")
plt.tight_layout()

output_image_path = "mapLungaDistanza.png"
plt.savefig(output_image_path)
plt.show()
