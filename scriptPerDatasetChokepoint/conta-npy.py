import os

def count_npy_files():
    # Ottieni il percorso della directory corrente
    current_directory = os.getcwd()

    # Variabile per il conteggio dei file .npy
    npy_file_count = 0

    # Esplora la directory corrente e tutte le sue sottocartelle
    for root, _, files in os.walk(current_directory):
        for file in files:
            # Verifica se il file ha estensione .npy
            if file.endswith('.npy'):
                npy_file_count += 1

    return npy_file_count

if __name__ == "__main__":
    total_npy_files = count_npy_files()
    print(f"Totale file .npy trovati: {total_npy_files}")
