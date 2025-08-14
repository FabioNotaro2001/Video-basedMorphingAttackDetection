import os
import pandas as pd

def aggrega_distanze(input_file, output_file):
    """ Aggrega le distanze coseno calcolando media, massimo e minimo per ID SOGGETTO, SEQUENZA e POSA,
        usando solo il secondo terzo delle righe per ciascun gruppo (senza riordinare). """
    
    df = pd.read_csv(input_file)
    gruppi = []

    for chiave, gruppo in df.groupby(["ID_SOGGETTO", "SEQUENZA", "POSA"]):
        n = len(gruppo)
        if n < 3:
            continue  # ignora i gruppi troppo piccoli

        x = n // 3
        if x == 0 or (n - 2 * x) == 0:
            continue  # niente da usare nel secondo terzo

        # Prende solo le righe centrali (secondo terzo)
        secondo_terzo = gruppo.iloc[x : n - x]

        if secondo_terzo.empty:
            continue

        media = secondo_terzo['SCORE'].mean()
        massimo = secondo_terzo['SCORE'].max()
        minimo = secondo_terzo['SCORE'].min()

        gruppi.append({
            "ID_SOGGETTO": chiave[0],
            "SEQUENZA": chiave[1],
            "POSA": chiave[2],
            "AVG": media,
            "MAX": massimo,
            "MIN": minimo
        })

    aggregated_df = pd.DataFrame(gruppi)
    aggregated_df.to_csv(output_file, index=False)
    print(f"File aggregato salvato in: {output_file}")

if __name__ == "__main__":
    dataset_root = os.getcwd()
    input_file = os.path.join(dataset_root, "genuineScores.txt")
    output_file = os.path.join(dataset_root, "mediumDistanceAggregatedGenuineScores.txt")
    
    if os.path.exists(input_file):
        aggrega_distanze(input_file, output_file)
    else:
        print(f"⚠️ Il file {input_file} non esiste. Esegui prima il calcolo delle distanze.")
