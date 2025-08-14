import os
import numpy as np
from scipy.spatial.distance import cosine

def load_vectors(base_path):
    vectors = {}
    for i in range(1, 66):  # Da ID001 a ID065
        folder_name = f"ID{i:03d}"
        icao_path = os.path.join(base_path, folder_name, "ICAO_photo")
        
        if os.path.exists(icao_path):
            npy_files = [f for f in os.listdir(icao_path) if f.endswith(".npy")]
            if npy_files:
                npy_path = os.path.join(icao_path, npy_files[0])  # Prende il primo file .npy trovato
                vectors[folder_name] = np.load(npy_path)
            else:
                print(f"Warning: No .npy file found in {icao_path}")
        else:
            print(f"Warning: {icao_path} not found!")
    return vectors

def compute_similarity(vectors):
    similarity_results = {}
    ids = list(vectors.keys())
    for id1 in ids:
        distances = []
        for id2 in ids:
            if id1 != id2:
                dist = cosine(vectors[id1], vectors[id2])
                distances.append((id2, dist))
        distances.sort(key=lambda x: x[1])  # Ordinamento per distanza crescente
        similarity_results[id1] = [id for id, _ in distances[:6]]  # Primi 6 più simili
    return similarity_results

def save_results(results, output_file):
    with open(output_file, "w") as f:
        for id, similar_ids in results.items():
            f.write(f"{id} {' '.join(similar_ids)}\n")

def main():
    base_path = "./"  # Modifica con il percorso del dataset
    output_file = "similarities.txt"
    
    vectors = load_vectors(base_path)
    if not vectors:
        print("No vectors found. Exiting.")
        return
    
    similarity_results = compute_similarity(vectors)
    save_results(similarity_results, output_file)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
