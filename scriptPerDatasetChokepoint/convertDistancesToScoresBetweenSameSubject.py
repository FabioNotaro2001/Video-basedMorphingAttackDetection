def aggiorna_valori(input_file, output_file):
    # Apre il file di input in modalità lettura e il file di output in modalità scrittura
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Leggi la prima riga (intestazione) e la scrivi nel file di output senza modificarla
        intestazione = infile.readline()
        outfile.write(intestazione)
        
        # Leggi il resto del file riga per riga
        for line in infile:
            # Split della riga in base al delimitatore ";"
            valori = line.strip().split(';')
            
            # Verifica che ci siano almeno 5 colonne (VIDEO ID, PERSON ID, AVG, MAX, MIN)
            if len(valori) >= 5:
                # Applica la formula per AVG, MAX e MIN (le ultime 3 colonne)
                for i in range(2, 5):
                    valori[i] = str(1 - (float(valori[i]) / 2))
                
                # Scrivi la riga aggiornata nel file di output
                outfile.write(';'.join(valori) + '\n')

# Esempio di utilizzo
input_file = 'aggregateAvgMaxMin.txt'  # Sostituisci con il percorso del file di input
output_file = 'scoresBetweenSameSubject.txt'  # Sostituisci con il percorso del file di output

aggiorna_valori(input_file, output_file)
