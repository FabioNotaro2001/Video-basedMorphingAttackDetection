import os
import pandas as pd

def aggrega_distanze(input_file, output_file):
    """Aggrega le distanze coseno calcolando media, massimo e minimo dell'ultimo terzo delle righe per ID SOGGETTO, SEQUENZA e POSA."""
    df = pd.read_csv(input_file)

    # Lista per i risultati aggregati
    aggregati = []

    # Raggruppa mantenendo l'ordine originale
    grouped = df.groupby(["ID_SOGGETTO", "SEQUENZA", "POSA"], sort=False)

    for (id_soggetto, sequenza, posa), group in grouped:
        n = len(group)
        if n < 3:
            continue  # Salta i gruppi troppo piccoli

        x = n // 3
        last_third = group.iloc[-x:]  # Prende solo l'ultimo terzo delle righe

        avg = last_third['SCORE'].mean()
        max_ = last_third['SCORE'].max()
        min_ = last_third['SCORE'].min()

        aggregati.append([id_soggetto, sequenza, posa, avg, max_, min_])

    # Crea DataFrame con i risultati
    aggregated_df = pd.DataFrame(aggregati, columns=["ID_SOGGETTO", "SEQUENZA", "POSA", "AVG", "MAX", "MIN"])

    # Salva il file
    aggregated_df.to_csv(output_file, index=False)
    print(f"File aggregato salvato in: {output_file}")

if __name__ == "__main__":
    dataset_root = os.getcwd()
    input_file = os.path.join(dataset_root, "genuineScores.txt")
    output_file = os.path.join(dataset_root, "shortDistanceAggregatedGenuineScores.txt")

    if os.path.exists(input_file):
        aggrega_distanze(input_file, output_file)
    else:
        print(f"⚠️ Il file {input_file} non esiste. Esegui prima il calcolo delle distanze.")
