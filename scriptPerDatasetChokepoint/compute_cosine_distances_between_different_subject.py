import os
import numpy as np
import random
from scipy.spatial.distance import cosine

def load_video_counts(file_path):
    """Carica il dizionario con ID persona e numero di video in cui appare."""
    if not os.path.isfile(file_path):
        print(f"Errore: il file '{file_path}' non esiste.")
        return {}
    
    video_counts = {}
    
    with open(file_path, 'r') as f:
        next(f)  # Salta la riga di intestazione
        
        for line in f:
            parts = line.strip().split(';')
            if len(parts) != 2:
                continue  # Salta righe malformattate
            
            person_id, video_count = parts
            try:
                video_counts[person_id] = int(video_count)
            except ValueError:
                print(f"Attenzione: valore non valido per {person_id}: {video_count}")
    
    return video_counts

def get_random_folder(base_folder, excluded_folders):
    """Seleziona casualmente una cartella che non sia 'groundtruth' e non sia già usata."""
    folders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f)) and f not in excluded_folders]
    return random.choice(folders) if folders else None

def get_valid_person_id(files, excluded_id, used_ids):
    """Ottiene un ID persona valido che non sia l'escluso e non sia già stato scelto."""
    person_ids = set(f.split('_')[1].split('.')[0] for f in files if '_' in f and f.endswith('.npy'))
    valid_ids = [pid for pid in person_ids if pid != excluded_id and pid not in used_ids]
    return random.choice(valid_ids) if valid_ids else None

def compute_cosine_distance(embedding1, embedding2):
    """Calcola la distanza coseno tra due embedding."""
    return cosine(embedding1, embedding2)

def process_embeddings(video_counts, embeddings_folder, dataset_folder, output_file):
    """Processa gli embedding e calcola le distanze coseno salvandole in un file di output."""
    if not os.path.isdir(embeddings_folder) or not os.path.isdir(dataset_folder):
        print("Errore: una delle cartelle specificate non esiste.")
        return
    
    with open(output_file, 'w') as f_out:
        f_out.write("PERSON ID;VIDEO ID;FRAME ID;OTHER PERSON ID;COSINE DISTANCE\n")
        
        for person_id, count in video_counts.items():
            embedding_file = os.path.join(embeddings_folder, f"ID{person_id}.npy")
            if not os.path.isfile(embedding_file):
                print(f"File embedding per {person_id} non trovato, saltato.")
                continue
            
            embedding = np.load(embedding_file)
            used_combinations = set()  # Set per tracciare coppie (cartella, OTHER PERSON ID)
            
            for _ in range(count):
                while True:
                    random_folder = get_random_folder(dataset_folder, {c for c, _ in used_combinations})
                    if not random_folder:
                        break
                    
                    folder_path = os.path.join(dataset_folder, random_folder)
                    files = [f for f in os.listdir(folder_path) if f.endswith('.npy')]
                    other_person_id = get_valid_person_id(files, person_id, {p for _, p in used_combinations if _ == random_folder})
                    
                    if other_person_id and (random_folder, other_person_id) not in used_combinations:
                        used_combinations.add((random_folder, other_person_id))
                        break  # Abbiamo trovato una coppia valida
                
                if not other_person_id:
                    continue
                
                for file in files:
                    if f"_{other_person_id}.npy" in file:
                        frame_id = file.split('_')[0]
                        other_embedding = np.load(os.path.join(folder_path, file))
                        cos_distance = compute_cosine_distance(embedding, other_embedding)
                        
                        f_out.write(f"{person_id};{random_folder};{frame_id};{other_person_id};{cos_distance}\n")

def main():
    # Sostituisci con il percorso reale dei file e delle cartelle
    file_path = "videosPerSubject.txt"
    embeddings_folder = "Still/Neutral"
    dataset_folder = "OriginalFiles"
    output_file = "cosineDistancesBetweenDifferentSubject.txt"
    
    video_counts = load_video_counts(file_path)
    process_embeddings(video_counts, embeddings_folder, dataset_folder, output_file)
    
if __name__ == "__main__":
    main()

