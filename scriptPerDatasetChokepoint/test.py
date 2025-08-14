import csv

def count_unique_pairs(file_path, target_person_id="0003"):
    unique_pairs = set()
    
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Salta l'intestazione
        
        for row in reader:
            if row[0] == target_person_id:
                video_id = row[1]
                other_person_id = row[3]
                unique_pairs.add((video_id, other_person_id))
    
    return len(unique_pairs)

# Sostituisci con il percorso corretto del file
txt_file_path = "cosineDistancesBetweenDifferentSubject.txt"
result = count_unique_pairs(txt_file_path)
print(f"Il PERSON ID 0005 compare in {result} coppie uniche di VIDEO ID e OTHER PERSON ID.")