def convert_distances_to_scores(input_file, output_file):
    with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
        lines = f_in.readlines()
        
        # Copia l'intestazione senza modificarla
        f_out.write(lines[0])
        
        for line in lines[1:]:  # Ignora la prima riga (intestazione)
            parts = line.strip().split(";")
            if len(parts) != 6:
                continue  # Salta righe malformattate
            
            person_id, other_id, sequence, mode, frame_id, cosine_distance = parts
            
            try:
                cosine_distance = float(cosine_distance)
                score = 1 - (cosine_distance / 2)
                f_out.write(f"{person_id};{other_id};{sequence};{mode};{frame_id};{score:.6f}\n")
            except ValueError:
                print(f"Warning: Invalid distance value in line - {line.strip()}")
                continue
    
    print(f"Converted file saved as {output_file}")

def main():
    input_file = "cosineDistancesBetweenDifferentSubjects.txt"  # File generato in precedenza
    output_file = "scoresBetweenDifferentSubjects.txt"  # File con i punteggi
    
    convert_distances_to_scores(input_file, output_file)

if __name__ == "__main__":
    main()
