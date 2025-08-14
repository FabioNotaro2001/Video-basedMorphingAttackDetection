import os

def convert_values_in_file(input_file, output_file):
    """Legge un file e converte i valori delle colonne AVG, MAX e MIN con la formula nuovoValore=1-(vecchioValore/2)."""
    if not os.path.isfile(input_file):
        print(f"Errore: il file '{input_file}' non esiste.")
        return
    
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        header = f_in.readline().strip()  # Legge l'intestazione
        f_out.write(header + "\n")  # Scrive l'intestazione nel nuovo file
        
        for line in f_in:
            parts = line.strip().split(';')
            if len(parts) != 6:
                continue  # Salta righe malformattate
            
            person_id, video_id, other_person_id, avg_val, max_val, min_val = parts
            try:
                avg_val = 1 - (float(avg_val) / 2)
                max_val = 1 - (float(max_val) / 2)
                min_val = 1 - (float(min_val) / 2)
                
                f_out.write(f"{person_id};{video_id};{other_person_id};{avg_val:.4f};{max_val:.4f};{min_val:.4f}\n")
            except ValueError:
                print(f"Attenzione: valore non valido nella riga: {line.strip()}")

def main():
    # Specifica i percorsi dei file
    input_file = "aggregateAvgMaxMinBetweenDifferentSubject.txt"  # File di input da convertire
    output_file = "scoresBetweenDifferentSubject.txt"  # File di output con i valori trasformati
    
    convert_values_in_file(input_file, output_file)
    
if __name__ == "__main__":
    main()
