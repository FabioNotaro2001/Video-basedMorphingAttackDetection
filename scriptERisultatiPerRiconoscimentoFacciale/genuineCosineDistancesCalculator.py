import os
import numpy as np
from scipy.spatial.distance import cosine

def estrai_frame_nome(file_name):
    """ Estrai il frame dal nome del file .npy """
    parts = file_name.split('-')
    if len(parts) > 2:
        return parts[-2]  # Il penultimo elemento
    return "Unknown"

def calcola_distanze(dataset_root, output_file):
    print(f"Analizzando il dataset nella cartella: {dataset_root}")
    print(f"Cartelle trovate: {os.listdir(dataset_root)}")
    """ Calcola la distanza coseno tra l'embedding della foto ICAO e le immagini delle sequenze video """
    with open(output_file, 'w') as f:
        print(f"Scrivendo i risultati in: {output_file}")

        f.write("ID_SOGGETTO,SEQUENZA,POSA,FRAME,DISTANZA_COSENO\n")
        
        for subject_folder in sorted(os.listdir(dataset_root)):
            subject_path = os.path.join(dataset_root, subject_folder)
            if not os.path.isdir(subject_path) or not subject_folder.startswith("ID"):
                continue

            icao_path = os.path.join(subject_path, "ICAO_photo")
            icao_embedding_path = None
            
            # Trova il file embedding nella cartella ICAO_photo
            for file in os.listdir(icao_path):
                if file.endswith(".npy"):
                    icao_embedding_path = os.path.join(icao_path, file)
                    break
            
            print(f"Analizzando soggetto: {subject_folder}")
            print(f"Percorso ICAO: {icao_path}")

            if not icao_embedding_path:
                print(f"⚠️ Nessun embedding ICAO trovato per {subject_folder}")
                continue

            
            icao_embedding = np.load(icao_embedding_path)
            
            for seq in ["sequence_01", "sequence_02"]:
                sequence_path = os.path.join(subject_path, "video_sequences", seq)
                if not os.path.exists(sequence_path):
                    continue
                
                for pose in ["frontal_gaze", "looking_around", "looking_around_with_occlusion"]:
                    pose_path = os.path.join(sequence_path, pose, "rgb")
                    if not os.path.exists(pose_path):
                        continue
                    
                    for file in sorted(os.listdir(pose_path)):
                        if file.endswith(".npy"):
                            embedding_path = os.path.join(pose_path, file)
                            embedding = np.load(embedding_path)
                            frame = estrai_frame_nome(file)
                            
                            # Calcola la distanza coseno
                            distance = cosine(icao_embedding, embedding)
                            
                            # Scrivi nel file
                            f.write(f"{subject_folder},{seq[-2:]},{pose},{frame},{distance:.6f}\n")
                            
    print(f"Distanze coseno salvate in {output_file}")

if __name__ == "__main__":
    print("Script avviato...")
    dataset_root = os.getcwd()  # Supponendo che lo script sia nella root del dataset
    output_file = os.path.join(dataset_root, "distanze_coseno.txt")
    calcola_distanze(dataset_root, output_file)
