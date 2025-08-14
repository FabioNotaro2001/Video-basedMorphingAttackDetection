import csv
from collections import defaultdict

def aggregate_cosine_distances(input_file, output_file):
    data = defaultdict(list)

    # Legge il file e aggrega i valori per chiave unica
    with open(input_file, "r") as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)  # Salta l'intestazione

        for row in reader:
            person_id, other_id, id_subject_in_frame, sequence, mode, _, cosine_distance = row
            key = (person_id, other_id, id_subject_in_frame, sequence, mode)
            data[key].append(float(cosine_distance))

    # Scrive il file con solo 1/3 dei valori per gruppo
    with open(output_file, "w", newline='') as f_out:
        writer = csv.writer(f_out, delimiter=';')
        writer.writerow(["PERSON ID", "OTHER PERSON ID", "SUBJECT_IN_FRAME_ID", "SEQUENCE", "MODE", "AVG", "MAX", "MIN", "COUNT_USED"])

        for key, values in data.items():
            subset_size = len(values) // 3
            if subset_size == 0:
                continue  # Salta gruppi troppo piccoli

            subset = values[:subset_size]
            avg_dist = sum(subset) / subset_size
            max_dist = max(subset)
            min_dist = min(subset)

            writer.writerow([*key, f"{avg_dist:.6f}", f"{max_dist:.6f}", f"{min_dist:.6f}", subset_size])

    print(f"Aggregated results saved to {output_file}")

def main():
    input_file = "impostorScores.txt"
    output_file = "longDistanceAggregatedImpostorScores.txt"  # Nuovo nome file output

    aggregate_cosine_distances(input_file, output_file)

if __name__ == "__main__":
    main()
