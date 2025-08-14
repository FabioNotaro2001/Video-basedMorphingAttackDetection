import csv
from collections import defaultdict

def aggregate_statistics(input_file, output_file):
    data = defaultdict(list)
    
    # Leggi il file di input e raccogli i dati raggruppati per (VIDEO ID, PERSON ID)
    with open(input_file, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Salta l'intestazione
        
        for row in reader:
            if len(row) != 4:
                continue  # Ignora righe non valide
            
            person_id, video_id, frame_id, cosine_distance = row
            try:
                cosine_distance = float(cosine_distance)
                data[(video_id, person_id)].append(cosine_distance)
            except ValueError:
                continue  # Ignora righe con dati non validi
    
    # Scrivi il file di output con le statistiche
    with open(output_file, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["VIDEO ID", "PERSON ID", "AVG", "MAX", "MIN"])
        
        for (video_id, person_id), distances in data.items():
            avg_distance = sum(distances) / len(distances)
            max_distance = max(distances)
            min_distance = min(distances)
            writer.writerow([video_id, person_id, f"{avg_distance:.4f}", f"{max_distance:.4f}", f"{min_distance:.4f}"])

# Esempio di utilizzo
input_file = "cosineDistancesBetweenSameSubject.txt"  # File generato dallo script precedente
output_file = "aggregateAvgMaxMinBetweenSameSubject.txt"  # File di output
aggregate_statistics(input_file, output_file)
