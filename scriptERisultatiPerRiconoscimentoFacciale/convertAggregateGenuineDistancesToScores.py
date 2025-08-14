import os
import pandas as pd

def converti_distanza_in_score(input_file, output_file):
    """ Legge il file aggregato e converte i valori di distanza in score usando la formula score=1-distanza/2. """
    # Carica il file di input in un DataFrame
    df = pd.read_csv(input_file)
    
    # Converte le colonne AVG, MAX, MIN in score
    df['AVG'] = 1 - df['AVG'] / 2
    df['MAX'] = 1 - df['MAX'] / 2
    df['MIN'] = 1 - df['MIN'] / 2
    
    # Salva il nuovo file
    df.to_csv(output_file, index=False)
    print(f"File con score salvato in: {output_file}")

if __name__ == "__main__":
    dataset_root = os.getcwd()  # Supponendo che sia nella root del dataset
    input_file = os.path.join(dataset_root, "aggregateCosineDistancesBetweenSameSubjects.txt")
    output_file = os.path.join(dataset_root, "aggregateScoresBetweenSameSubjects.txt")
    
    if os.path.exists(input_file):
        converti_distanza_in_score(input_file, output_file)
    else:
        print(f"⚠️ Il file {input_file} non esiste. Esegui prima l'aggregazione delle distanze.")
