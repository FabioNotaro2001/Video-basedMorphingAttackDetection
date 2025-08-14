import os

def count_videos_per_subject(input_file, output_file):
    if not os.path.isfile(input_file):
        print(f"Errore: il file '{input_file}' non esiste.")
        return
    
    subject_videos = {}
    
    with open(input_file, 'r') as f:
        next(f)  # Salta la riga di intestazione
        
        for line in f:
            parts = line.strip().split(';')
            if len(parts) != 4:
                continue  # Salta righe malformattate
            
            person_id, video_id, _, _ = parts
            
            if person_id not in subject_videos:
                subject_videos[person_id] = set()
            
            subject_videos[person_id].add(video_id)
    
    with open(output_file, 'w') as f_out:
        f_out.write("PERSON ID;VIDEOS\n")
        for person_id, videos in subject_videos.items():
            f_out.write(f"{person_id};{len(videos)}\n")
    
    print(f"File '{output_file}' generato con successo.")

# Esempio di utilizzo: sostituisci con il percorso reale dei file
input_file = "cosineDistancesBetweenSameSubject.txt"
output_file = "videosPerSubject.txt"
count_videos_per_subject(input_file, output_file)
