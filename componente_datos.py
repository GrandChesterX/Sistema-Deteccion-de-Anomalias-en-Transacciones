import pandas as pd
from datetime import datetime

def cargar_y_validar_transacciones(filepath_or_buffer) -> pd.DataFrame:
    # 1. Ingesta: Intentar leer el archivo CSV
    try:
        df = pd.read_csv(filepath_or_buffer, sep=';', encoding='utf-8-sig') # separador de columnas es punto y coma
        df.columns = df.columns.str.strip() # Quitar espacios en blanco de los nombres de las columnas
        # Limpiar espacios y nulos en el área del hospital
        df["id_transaccion"] = df["id_transaccion"].fillna("No especificado").astype(str).str.strip() # estamos asumiendo que el id_transaccion es un string, si no lo es, se puede cambiar a int o float  
    except Exception as error:
        raise ValueError(f"Error crítico al leer el archivo CSV: {error}")
    
    columnas_separadas = [
        "id_transaccion",
        "fecha_hora",
        "monto_eur",
        "distancia_km_cliente",
    ]
    # Elimina cualquier fila del archivo que esté completamente vacía
    df = df.dropna(how='all')#estamos eliminando las filas que estén completamente vacías, si hay alguna fila que tenga al menos un valor, no se eliminará
    faltantes = [col for col in columnas_separadas if col not in df.columns] #estamos verificando si todas las columnas que necesitamos están presentes en el dataframe, si no lo están, se guardan en la lista faltantes
    if faltantes:
        raise ValueError(f"Contrato incumplido. Faltan las siguientes columnas: {faltantes}")
    
    try:
        df["id_transaccion"] = df["id_transaccion"].astype(str)
        df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], format="%d-%m-%y %H:%M")
        df["monto_eur"] = (
            df["monto_eur"].astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype("float64")
        )
        df["distancia_km_cliente"] = df["distancia_km_cliente"].astype("float64")
    except Exception as error:
        raise ValueError(f"Contrato incumplido: Error al convertir los tipos de datos {error}")

#4. Validacion de Reglas Logicas y Matematicas
    
    # Codigo unico para cada transaccion
    id_transaccion = df["id_transaccion"]
    if id_transaccion.duplicated().any():
        raise ValueError("Contrato incumplido: Existen registros con id_transaccion duplicados")
    # Momento exacto de la transaccion con horas
    fecha_actual = pd.to_datetime(datetime.today())
    if (df["fecha_hora"] > fecha_actual).any():
        raise ValueError("Contrato incumplido: no se han proporcionado los momentos exactos.")
    
    #Valor de la compra debe ser mayor a 0
    if (df["monto_eur"] <= 0).any():
        raise ValueError("Contrato incumplido: Existen registros con monto 0 o negativo")

    # Distancia del cliente debe ser mayor a 0
    if (df["distancia_km_cliente"] < 0).any():
        raise ValueError("Contrato incumplido: Existen registros con distancia negativa")
    
    return df