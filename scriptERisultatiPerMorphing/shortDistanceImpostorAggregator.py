import csv
from collections import defaultdict, deque

def aggregate_cosine_distances(input_file, output_file):
    data = defaultdict(list)
    
    # Legge il file e raggruppa le righe per chiave
    with open(input_file, "r") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # Salta l'intestazione
        
        for row in reader:
            person_id, other_id, id_subject_in_frame, sequence, mode, _, cosine_distance = row
            key = (person_id, other_id, id_subject_in_frame, sequence, mode)
            data[key].append(float(cosine_distance))
    
    # Calcola le statistiche usando solo le ultime X righe (dove X = numero di righe del gruppo)
    with open(output_file, "w", newline='') as f_out:
        writer = csv.writer(f_out, delimiter=';')
        writer.writerow(["PERSON ID", "OTHER PERSON ID", "SUBJECT_IN_FRAME_ID", "SEQUENCE", "MODE", "AVG", "MAX", "MIN"])
        
        for key, values in data.items():
            x = len(values)
            # Prendiamo solo le ultime X righe (in pratica è l’intero gruppo)
            last_x_values = values[-x:]  # Qui è equivalente a values, ma lascia aperta la porta a una logica futura più selettiva
            avg_dist = sum(last_x_values) / len(last_x_values)
            max_dist = max(last_x_values)
            min_dist = min(last_x_values)
            writer.writerow([*key, f"{avg_dist:.6f}", f"{max_dist:.6f}", f"{min_dist:.6f}"])
    
    print(f"Aggregated results saved to {output_file}")

def main():
    input_file = "impostorScores.txt"
    output_file = "shortDistanceAggregatedImpostorScores.txt"
    
    aggregate_cosine_distances(input_file, output_file)

if __name__ == "__main__":
    main()
