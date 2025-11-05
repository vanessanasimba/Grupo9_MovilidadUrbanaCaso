import pandas as pd
import os

# ruta absoluta de la carpeta donde esta el script (../scripts)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ruta absoluta de la carpeta data donde se encuntra el dataset (../data)
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "data","yellow_tripdata_2015-01.csv")

# creacion de la funcion para cargar los datos
def cargar_datos(path):
    """
    Carga una muestra del dataset (20,000 filas) para evitar errores de memoria.
    """
    print(f"Cargando muestra de 20,000 filas desde: {path}")
    try:
        df = pd.read_csv(path, sep=",", encoding="utf-8", nrows=20000, on_bad_lines="skip", low_memory=False)
        print(f"✅ Datos cargados exitosamente. Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
        return df
    except FileNotFoundError:
        print(f"❌ El archivo no se encontró en la ruta: {path}")
        return None
    except pd.errors.EmptyDataError:
        print("❌ El archivo está vacío.")
        return None
    except pd.errors.ParserError as e:
        print(f"❌ Error al parsear el archivo CSV:\n{e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

