import os

def compute_average_videos_per_subject(file_path):
    if not os.path.isfile(file_path):
        print(f"Errore: il file '{file_path}' non esiste.")
        return
    
    subject_videos = {}
    
    with open(file_path, 'r') as f:
        next(f)  # Salta la riga di intestazione
        
        for line in f:
            parts = line.strip().split(';')
            if len(parts) != 4:
                continue  # Salta righe malformattate
            
            person_id, video_id, _, _ = parts
            
            if person_id not in subject_videos:
                subject_videos[person_id] = set()
            
            subject_videos[person_id].add(video_id)
    
    if not subject_videos:
        print("Nessun dato valido trovato nel file.")
        return
    
    total_videos = sum(len(videos) for videos in subject_videos.values())
    total_subjects = len(subject_videos)
    average_videos = total_videos / total_subjects
    
    print(f"Media dei VIDEO ID per ogni ID SOGGETTO: {average_videos:.2f}")

# Esempio di utilizzo: sostituisci con il percorso reale del file
file_path = "cosineDistancesBetweenSameSubject.txt"
compute_average_videos_per_subject(file_path)
