import os
import numpy as np
from collections import defaultdict

def process_cosine_distances(input_file, output_file):
    """Raggruppa i dati per (PERSON ID, VIDEO ID, OTHER PERSON ID) e calcola AVG, MAX, MIN delle distanze coseno."""
    if not os.path.isfile(input_file):
        print(f"Errore: il file '{input_file}' non esiste.")
        return
    
    data = defaultdict(list)
    
    # Legge il file e raggruppa le distanze coseno
    with open(input_file, 'r') as f:
        next(f)  # Salta l'intestazione
        for line in f:
            parts = line.strip().split(';')
            if len(parts) != 5:
                continue  # Salta righe malformattate
            
            person_id, video_id, frame_id, other_person_id, cos_distance = parts
            try:
                cos_distance = float(cos_distance)
                data[(person_id, video_id, other_person_id)].append(cos_distance)
            except ValueError:
                print(f"Attenzione: valore non valido nella riga: {line.strip()}")
    
    # Scrive i risultati aggregati nel file di output
    with open(output_file, 'w') as f_out:
        f_out.write("PERSON ID;VIDEO ID;OTHER PERSON ID;AVG;MAX;MIN\n")
        
        for (person_id, video_id, other_person_id), distances in data.items():
            avg_distance = np.mean(distances)
            max_distance = np.max(distances)
            min_distance = np.min(distances)
            f_out.write(f"{person_id};{video_id};{other_person_id};{avg_distance:.4f};{max_distance:.4f};{min_distance:.4f}\n")

def main():
    # Specifica i percorsi dei file
    input_file = "cosineDistancesBetweenDifferentSubject.txt"
    output_file = "aggregateAvgMaxMinBetweenDifferentSubject.txt"
    
    process_cosine_distances(input_file, output_file)
    
if __name__ == "__main__":
    main()
