import pandas as pd

def calcular_kpis_fraude(df: pd.DataFrame) -> dict:

    """
    Calcula los KPIs de fraude a partir de un DataFrame de trans
    """
    if df.empty:
        return {
            "volumen_total_eur": 0,
            "ticket_promedio": 0,
            "cantidad_transacciones": 0
        }
        
   # retorno volumen total de transacciones en euros
    volumen_total_eur = float(df['monto_eur'].sum())   
    # retorno ticket promedio total de transacciones
    ticket_promedio = float(df['monto_eur'].mean())
    # retorno cantidad total de transacciones
    cantidad_transacciones = len(df)

    return {
        "volumen_total_eur": volumen_total_eur, 
        "ticket_promedio": ticket_promedio,
        "cantidad_transacciones": cantidad_transacciones
    }