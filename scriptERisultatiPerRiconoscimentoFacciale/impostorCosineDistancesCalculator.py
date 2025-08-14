import os
import numpy as np
import random
from scipy.spatial.distance import cosine

def load_icao_vector(base_path, person_id):
    npy_path = os.path.join(base_path, person_id, "ICAO_photo")
    npy_files = [f for f in os.listdir(npy_path) if f.endswith(".npy")]
    if npy_files:
        return np.load(os.path.join(npy_path, npy_files[0]))  # Prende il primo .npy
    return None

def extract_frame_id(filename):
    parts = filename.split('-')
    if len(parts) >= 2:
        return parts[-2]  # Penultimo elemento
    return "unknown"

def get_valid_rgb_path(base_path, other_id):
    sequences = ["sequence_01", "sequence_02"]
    modes = ["frontal_gaze", "looking_around", "looking_around_with_occlusion"]
    random.shuffle(sequences)
    random.shuffle(modes)
    
    for sequence in sequences:
        for mode in modes:
            rgb_path = os.path.join(base_path, other_id, "video_sequences", sequence, mode, "rgb")
            if os.path.exists(rgb_path):
                return rgb_path, sequence, mode
    return None, None, None

def compute_distances(base_path, similarities_file, output_file):
    with open(similarities_file, "r") as f:
        similarity_lines = f.readlines()
    
    with open(output_file, "w") as f_out:
        f_out.write("PERSON ID;OTHER PERSON ID;SEQUENCE;MODE;FRAME ID;COSINE DISTANCE\n")
        
        for idx, line in enumerate(similarity_lines, start=1):
            data = line.strip().split()
            if len(data) < 2:
                continue
            
            person_id = data[0]  # ID del soggetto ICAO
            similar_ids = data[1:7]  # I 6 ID più simili
            print(f"Processing {idx}/{len(similarity_lines)}: {person_id}")
            
            icao_vector = load_icao_vector(base_path, person_id)
            if icao_vector is None:
                print(f"Warning: No ICAO vector for {person_id}")
                continue
            
            for other_id in similar_ids:
                rgb_path, sequence, mode = get_valid_rgb_path(base_path, other_id)
                
                if rgb_path is None:
                    print(f"Warning: No valid path found for {other_id}")
                    continue
                
                npy_files = [f for f in os.listdir(rgb_path) if f.endswith(".npy")]
                for npy_file in npy_files:
                    npy_vector = np.load(os.path.join(rgb_path, npy_file))
                    frame_id = extract_frame_id(npy_file)
                    cos_distance = cosine(icao_vector, npy_vector)
                    
                    f_out.write(f"{person_id};{other_id};{sequence[-2:]};{mode};{frame_id};{cos_distance:.6f}\n")
    
    print(f"Results saved to {output_file}")

def main():
    base_path = "./"  # Modifica con il percorso del dataset
    similarities_file = "similarities.txt"  # Il file generato dallo script precedente
    output_file = "cosine_distances.txt"
    
    compute_distances(base_path, similarities_file, output_file)

if __name__ == "__main__":
    main()
