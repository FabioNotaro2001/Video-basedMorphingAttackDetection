import os
import pandas as pd

def aggrega_distanze(input_file, output_file):
    """ Aggrega le distanze coseno calcolando media, massimo e minimo per ID SOGGETTO, SEQUENZA e POSA. """
    # Carica il file di input in un DataFrame
    df = pd.read_csv(input_file)
    
    # Raggruppa per ID_SOGGETTO, SEQUENZA, POSA e calcola le statistiche
    aggregated_df = df.groupby(["ID_SOGGETTO", "SEQUENZA", "POSA"])['SCORE'].agg(['mean', 'max', 'min']).reset_index()
    
    # Rinomina le colonne
    aggregated_df.columns = ["ID_SOGGETTO", "SEQUENZA", "POSA", "AVG", "MAX", "MIN"]
    
    # Salva il nuovo file
    aggregated_df.to_csv(output_file, index=False)
    print(f"File aggregato salvato in: {output_file}")

if __name__ == "__main__":
    dataset_root = os.getcwd()  # Supponendo che sia nella root del dataset
    input_file = os.path.join(dataset_root, "genuineScores.txt")
    output_file = os.path.join(dataset_root, "aggregatedGenuineScores.txt")
    
    if os.path.exists(input_file):
        aggrega_distanze(input_file, output_file)
    else:
        print(f"⚠️ Il file {input_file} non esiste. Esegui prima il calcolo delle distanze.")