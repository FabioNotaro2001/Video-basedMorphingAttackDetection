import os
import pandas as pd

def aggrega_distanze(input_file, output_file):
    """Aggrega le distanze coseno usando solo il primo terzo di ogni gruppo (ID_SOGGETTO, SEQUENZA, POSA)."""
    df = pd.read_csv(input_file)

    gruppi = df.groupby(["ID_SOGGETTO", "SEQUENZA", "POSA"])
    risultati = []

    for chiave, gruppo in gruppi:
        n = len(gruppo)
        limite = max(1, n // 3)  # almeno 1 elemento per sicurezza
        subset = gruppo.iloc[:limite]  # prende il primo terzo

        media = subset["SCORE"].mean()
        massimo = subset["SCORE"].max()
        minimo = subset["SCORE"].min()

        risultati.append((*chiave, media, massimo, minimo))

    aggregated_df = pd.DataFrame(risultati, columns=["ID_SOGGETTO", "SEQUENZA", "POSA", "AVG", "MAX", "MIN"])
    aggregated_df.to_csv(output_file, index=False)
    print(f"File aggregato salvato in: {output_file}")

if __name__ == "__main__":
    dataset_root = os.getcwd()
    input_file = os.path.join(dataset_root, "genuineScores.txt")
    output_file = os.path.join(dataset_root, "longDistanceAggregatedGenuineScores.txt")
    
    if os.path.exists(input_file):
        aggrega_distanze(input_file, output_file)
    else:
        print(f"⚠️ Il file {input_file} non esiste. Esegui prima il calcolo delle distanze.")
