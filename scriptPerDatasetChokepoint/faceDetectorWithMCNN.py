import os
from mtcnn import MTCNN
from PIL import Image
import cv2

# Crea un oggetto MTCNN globale
detector = MTCNN()

def detect_faces_with_mtcnn(image_path):
    """
    Rileva volti in un'immagine utilizzando MTCNN.
    
    Args:
        image_path (str): Percorso dell'immagine.
        
    Returns:
        bool: True se viene rilevato almeno un volto, False altrimenti.
    """
    try:
        # Carica l'immagine
        image = cv2.imread(image_path)
        if image is None:
            return False  # Salta se l'immagine non è valida
        
        # Converti in RGB (MTCNN lavora meglio con RGB)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Usa MTCNN per rilevare volti
        faces = detector.detect_faces(image_rgb)
        
        return len(faces) > 0  # True se trova almeno un volto
    except Exception as e:
        print(f"Errore durante l'elaborazione di {image_path}: {e}")
        return False

def process_folder(folder_path):
    """
    Analizza una cartella e elimina le immagini che non contengono volti.
    
    Args:
        folder_path (str): Percorso della cartella da analizzare.
    """
    # Ottieni tutti i file immagine nella cartella
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
    
    for file_path in files:
        if not detect_faces_with_mtcnn(file_path):
            # Elimina il file se non contiene volti
            os.remove(file_path)
            print(f"Eliminato: {file_path}")
        else:
            print(f"Conservato: {file_path}")

def process_all_subfolders(base_path):
    """
    Analizza tutte le sottocartelle in una directory e processa ciascuna di esse.
    
    Args:
        base_path (str): Percorso della directory principale contenente le sottocartelle.
    """
    # Trova tutte le sottocartelle
    subfolders = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    for folder in subfolders:
        print(f"Analizzando la cartella: {folder}")
        process_folder(folder)

if __name__ == "__main__":
    # Percorso della directory contenente le sottocartelle
    base_directory = os.path.dirname(os.path.abspath(__file__))
    process_all_subfolders(base_directory)
