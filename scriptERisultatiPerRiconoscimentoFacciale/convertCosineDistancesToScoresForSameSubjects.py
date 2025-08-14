import os

def converti_distanza_in_score(input_file, output_file):
    """ Legge il file di input, calcola il nuovo score e salva il risultato in un nuovo file """
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        lines = f_in.readlines()
        
        if not lines:
            print("⚠️ Il file di input è vuoto!")
            return
        
        # Scrivi l'intestazione senza modifiche
        f_out.write(lines[0])
        
        # Processa ogni riga, ignorando l'intestazione
        for line in lines[1:]:
            parts = line.strip().split(',')
            if len(parts) != 5:
                print(f"⚠️ Riga ignorata per formato errato: {line.strip()}")
                continue
            
            id_soggetto, sequenza, posa, frame, distanza_coseno = parts
            try:
                distanza_coseno = float(distanza_coseno)
                score = 1 - distanza_coseno / 2
                f_out.write(f"{id_soggetto},{sequenza},{posa},{frame},{score:.6f}\n")
            except ValueError:
                print(f"⚠️ Impossibile convertire la distanza in numero: {distanza_coseno}")
                continue

    print(f"✅ File convertito e salvato come {output_file}")

if __name__ == "__main__":
    dataset_root = os.getcwd()  # Assumiamo che lo script sia nella stessa cartella del file input
    input_file = os.path.join(dataset_root, "cosineDistancesBetweenSameSubjects.txt")
    output_file = os.path.join(dataset_root, "scoresBetweenSameSubjects.txt")
    
    if os.path.exists(input_file):
        converti_distanza_in_score(input_file, output_file)
    else:
        print(f"❌ Il file {input_file} non esiste! Assicurati di eseguire prima lo script di calcolo distanze.")
