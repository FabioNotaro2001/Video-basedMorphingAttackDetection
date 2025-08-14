import csv
from collections import defaultdict

def aggregate_cosine_distances(input_file, output_file):
    data = defaultdict(list)
    
    # Legge il file e aggrega i valori per chiave unica (PERSON ID, OTHER PERSON ID, SUBJECT_IN_FRAME_ID, SEQUENCE, MODE)
    with open(input_file, "r") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # Salta l'intestazione
        
        for row in reader:
            person_id, other_id, id_subject_in_frame, sequence, mode, _, cosine_distance = row
            key = (person_id, other_id, id_subject_in_frame, sequence, mode)
            data[key].append(float(cosine_distance))
    
    # Calcola le statistiche e scrive il nuovo file
    with open(output_file, "w", newline='') as f_out:
        writer = csv.writer(f_out, delimiter=';')
        writer.writerow(["PERSON ID", "OTHER PERSON ID", "SUBJECT_IN_FRAME_ID", "SEQUENCE", "MODE", "AVG", "MAX", "MIN"])
        
        for key, values in data.items():
            avg_dist = sum(values) / len(values)
            max_dist = max(values)
            min_dist = min(values)
            writer.writerow([*key, f"{avg_dist:.6f}", f"{max_dist:.6f}", f"{min_dist:.6f}"])
    
    print(f"Aggregated results saved to {output_file}")

def main():
    input_file = "impostorScores.txt"  # Il file di input
    output_file = "aggregatedImpostorScores.txt"  # Il file di output
    
    aggregate_cosine_distances(input_file, output_file)

if __name__ == "__main__":
    main()
