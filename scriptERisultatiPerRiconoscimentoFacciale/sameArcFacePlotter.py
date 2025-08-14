import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D

# Mappa categorie → colori
CATEGORIES = {
    os.path.normpath("ICAO_photo"): "red",
    os.path.normpath("non_ICAO_frontal_photos"): "blue",
    os.path.normpath("sequence_01/frontal_gaze"): "green",
    os.path.normpath("sequence_01/looking_around"): "orange",
    os.path.normpath("sequence_01/looking_around_with_occlusion"): "purple",
    os.path.normpath("sequence_02/frontal_gaze"): "cyan",
    os.path.normpath("sequence_02/looking_around"): "magenta",
    os.path.normpath("sequence_02/looking_around_with_occlusion"): "brown",
}

def get_category_from_path(path):
    path_parts = os.path.normpath(path).split(os.sep)
    for category in CATEGORIES:
        category_parts = category.split(os.sep)
        if all(part in path_parts for part in category_parts):
            return category
    return None

def load_embeddings(base_dir):
    embeddings = []
    labels = []

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".npy"):
                full_path = os.path.join(root, file)
                category = get_category_from_path(full_path)
                if category:
                    embedding = np.load(full_path)
                    if embedding.shape == (512,):
                        embeddings.append(embedding)
                        labels.append(category)
    return np.array(embeddings), labels

def plot_tsne_3d(embeddings, labels, save_path="tsne_plot_3d.png"):
    print("Eseguendo t-SNE 3D...")
    tsne = TSNE(n_components=3, random_state=42, perplexity=30)
    reduced = tsne.fit_transform(embeddings)

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    for category, color in CATEGORIES.items():
        idxs = [i for i, lbl in enumerate(labels) if lbl == category]
        if idxs:
            ax.scatter(
                reduced[idxs, 0], reduced[idxs, 1], reduced[idxs, 2],
                c=color, label=category.replace(os.sep, '/'), alpha=0.6
            )

    ax.set_title("ARCFACE EMBEDDING RELATED TO SUBJECT ID065")
    ax.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Plot 3D salvato in: {save_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    embeddings, labels = load_embeddings(base_dir)
    if embeddings.size == 0:
        print("Nessun embedding trovato.")
    else:
        plot_tsne_3d(embeddings, labels)
