def remove_last_column(file_path: str, separator: str = ';') -> None:
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Rimuove l'ultima colonna da ogni riga
    new_lines = []
    for line in lines:
        parts = line.strip().split(separator)
        if len(parts) > 1:
            new_line = separator.join(parts[:-1])  # Tutto tranne l'ultima colonna
            new_lines.append(new_line + '\n')

    # Sovrascrive il file
    with open(file_path, 'w') as file:
        file.writelines(new_lines)

# ESEMPIO DI UTILIZZO:
file_path = 'longDistanceAggregatedImpostorScores.txt'
remove_last_column(file_path)
