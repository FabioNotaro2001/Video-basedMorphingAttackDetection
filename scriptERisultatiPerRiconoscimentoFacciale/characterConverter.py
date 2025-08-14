def sostituisci_virgole_con_punto_e_virgola(nome_file):
    try:
        with open(nome_file, 'r', encoding='utf-8') as file:
            contenuto = file.read()
        
        contenuto_modificato = contenuto.replace(',', ';')
        
        with open(nome_file, 'w', encoding='utf-8') as file:
            file.write(contenuto_modificato)
        
        print(f"Sostituzione completata nel file '{nome_file}'.")

    except FileNotFoundError:
        print(f"Errore: Il file '{nome_file}' non è stato trovato.")
    except Exception as e:
        print(f"Errore durante l'elaborazione: {e}")

# Esempio di utilizzo:
if __name__ == "__main__":
    sostituisci_virgole_con_punto_e_virgola("aggregatedGenuineScores.txt")
