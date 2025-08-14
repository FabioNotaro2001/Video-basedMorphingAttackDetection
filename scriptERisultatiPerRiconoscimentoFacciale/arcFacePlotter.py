import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D

# Root directory (dove metti questo script)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Lista per embeddings e labels
embeddings = []
labels = []

# Scorri le cartelle ID001-ID065
for folder_name in sorted(os.listdir(ROOT_DIR)):
    folder_path = os.path.join(ROOT_DIR, folder_name)
    if os.path.isdir(folder_path) and folder_name.startswith("ID"):
        icao_path = os.path.join(folder_path, "ICAO_photo")
        if os.path.isdir(icao_path):
            for file in os.listdir(icao_path):
                if file.endswith(".npy"):
                    embedding_path = os.path.join(icao_path, file)
                    embedding = np.load(embedding_path)
                    embeddings.append(embedding)
                    labels.append(folder_name)

# Converti in array
embeddings = np.array(embeddings)

# Riduzione a 3D con t-SNE
tsne = TSNE(n_components=3, perplexity=15, random_state=42)
embeddings_3d = tsne.fit_transform(embeddings)

# Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

for i, label in enumerate(labels):
    ax.scatter(*embeddings_3d[i], label=label)

# Evita di mettere 65 etichette nella legenda
ax.set_title("3D DISTRIBUTION OF ARCFACE EMBEDDINGS AFTER T-SNE DIMENSIONALITY REDUCTION")
#ax.set_xlabel("Dimensione 1")
#ax.set_ylabel("Dimensione 2")
#ax.set_zlabel("Dimensione 3")

# Salva la figura
plt.savefig("embedding_3d_plot.png", dpi=300)
plt.show()
