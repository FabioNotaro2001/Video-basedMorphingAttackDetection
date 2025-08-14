import csv

def convert_distances_to_scores(input_file, output_file):
    with open(input_file, "r") as f_in, open(output_file, "w", newline='') as f_out:
        reader = csv.reader(f_in, delimiter=';')
        writer = csv.writer(f_out, delimiter=';')
        
        header = next(reader, None)  # Legge l'intestazione
        if header:
            writer.writerow(header)  # Scrive l'intestazione invariata
        
        for row in reader:
            if len(row) < 7:
                continue  # Salta eventuali righe vuote
            
            person_id, other_id, sequence, mode, avg, max_val, min_val = row
            
            # Converte distanza in score
            avg_score = 1 - float(avg) / 2
            max_score = 1 - float(max_val) / 2
            min_score = 1 - float(min_val) / 2
            
            writer.writerow([person_id, other_id, sequence, mode, f"{avg_score:.6f}", f"{max_score:.6f}", f"{min_score:.6f}"])
    
    print(f"Converted results saved to {output_file}")

def main():
    input_file = "aggregatedCosineDistancesBetweenDifferentSubjects.txt"  # Il file con distanze
    output_file = "aggregatedScoresBetweenDifferentSubjects.txt"  # Il file con gli score
    
    convert_distances_to_scores(input_file, output_file)

if __name__ == "__main__":
    main()
