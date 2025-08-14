import os
import numpy as np
from scipy.spatial.distance import cosine

def load_embeddings(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Errore: la cartella '{folder_path}' non esiste.")
        return {}
    
    npy_files = [f for f in os.listdir(folder_path) if f.endswith('.npy')]
    
    if not npy_files:
        print("Nessun file .npy trovato nella cartella.")
        return {}
    
    embeddings_dict = {}
    
    for file in npy_files:
        file_path = os.path.join(folder_path, file)
        try:
            embedding = np.load(file_path)
            if embedding.shape != (512,):
                continue
            
            file_id = os.path.splitext(file)[0][2:]
            
            embeddings_dict[file_id] = embedding
        except Exception as e:
            print(f"Errore nel caricamento del file {file}: {e}")
    
    return embeddings_dict

def process_subfolders(main_folder_path, embeddings_dict, output_file):
    if not os.path.isdir(main_folder_path):
        print(f"Errore: la cartella '{main_folder_path}' non esiste.")
        return
    
    with open(output_file, 'w') as f:
        f.write("PERSON ID;VIDEO ID;FRAME ID;COSINE DISTANCE\n")
        
        for subfolder in os.listdir(main_folder_path):
            subfolder_path = os.path.join(main_folder_path, subfolder)
            
            if not os.path.isdir(subfolder_path):
                continue
            
            for file in os.listdir(subfolder_path):
                if file.endswith('.npy'):
                    file_path = os.path.join(subfolder_path, file)
                    
                    try:
                        embedding = np.load(file_path)
                        if embedding.shape != (512,):
                            continue
                        
                        parts = file.split('_')
                        if len(parts) != 2:
                            continue
                        
                        numeroFrame = parts[0]
                        idSoggetto = os.path.splitext(parts[1])[0]
                        
                        if idSoggetto in embeddings_dict:
                            original_embedding = embeddings_dict[idSoggetto]
                            cos_distance = cosine(original_embedding, embedding)
                            
                            f.write(f"{idSoggetto};{subfolder};{numeroFrame};{cos_distance:.4f}\n")
                    except Exception as e:
                        print(f"Errore nel caricamento del file {file} in {subfolder}: {e}")

folder_path = "Still/Neutral"
main_folder_path = "OriginalFiles"
output_file = "cosineDistancesBetweenSameSubject.txt"

embeddings = load_embeddings(folder_path)
process_subfolders(main_folder_path, embeddings, output_file)



