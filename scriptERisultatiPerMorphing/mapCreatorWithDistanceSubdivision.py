import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# === 1) Lettura del file ====================================================
file_path = "impostorScores.txt"
df = pd.read_csv(file_path, header=None, skiprows=1)
df.columns = ['subject1', 'subject2', 'probe_subject', 'sequenza', 'posa', 'frame', 'score']

# === 2) Identificatore del morph e conteggi =================================
df['morph_id'] = list(zip(df['subject1'], df['subject2']))
group_counts = df.groupby(['morph_id', 'probe_subject']).size()
m_min_per_morph = group_counts.groupby(level=0).min()
m_min = m_min_per_morph.min()

triples_min = group_counts[group_counts == m_min].index.to_list()
print(f"m_min (numero minimo di probe per soggetto su tutti i morph): {m_min}")
print("Triple che realizzano m_min:")
for (s1, s2), probe_subj in triples_min:
    print(f"  (subject1={s1}, subject2={s2}, probe_subject={probe_subj})")

# === 3) Parametri ===========================================================
threshold = 0.49320          # soglia ArcFace
r_values = [1, 10, 25, 50, 100, 200, 300]

# === 4) Calcolo MAP modificato ==============================================
map_values = []
morph_groups = df.groupby('morph_id')

for r in r_values:
    valid_morphs = 0
    success_morphs = 0

    if r == 1:
        # Caso r=1 come prima
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

    else:
        # Divisione in 3 parti a livello del gruppo morph_id, senza sotto-raggruppamenti
        r_parts = [r // 3] * 3
        r_parts[-1] += r % 3

        def sample_three_parts(arr, parts):
            splits = np.array_split(arr, 3)
            samples = []
            for split, part in zip(splits, parts):
                if len(split) < part:
                    return None
                samples.extend(np.random.choice(split, part, replace=False))
            return np.array(samples)

        for morph_id, group in morph_groups:
            subj1, subj2 = morph_id
            sel1_scores = group[group['probe_subject'] == subj1].sort_values(by='frame')['score'].values
            sel2_scores = group[group['probe_subject'] == subj2].sort_values(by='frame')['score'].values

            if len(sel1_scores) < r or len(sel2_scores) < r:
                continue  # non valido

            sel1 = sample_three_parts(sel1_scores, r_parts)
            sel2 = sample_three_parts(sel2_scores, r_parts)

            if sel1 is None or sel2 is None:
                continue  # non valido

            valid_morphs += 1
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
            cbar=False)

plt.title("Morphing Attack Potential (MAP) with distance uniformity")
plt.ylabel("Verification attempts (r)")
plt.tight_layout()

output_image_path = "mapConDistanze.png"
plt.savefig(output_image_path)
plt.show()
