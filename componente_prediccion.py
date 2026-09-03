import pandas as pd

# detectar_anomalias(df) Retorna una lista  de transacciones fraudalentas. Una transaccion es fraude  si distancia_km_cliente > 500 o si monto_eur > 5000

def detectar_anomalias(df: pd.DataFrame) -> list:


    if df.empty:
        return []
    
    transacciones_fraudulentas = df[(df['distancia_km_cliente'] > 500) | (df['monto_eur'] > 5000)]
    return transacciones_fraudulentas.to_dict(orient='records')
    