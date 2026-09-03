import streamlit as st
import pandas as pd

import componente_datos as cd
import componente_metricas as cm
import componente_prediccion as cp


st.set_page_config(page_title="Analizador de TransAcciones", page_icon="💵", layout="wide")
st.title("💸 Sistema en Tiempo Real de Deteccion de Anomalias en Transacciones")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configuración")
    archivo_subido = st.file_uploader("Sube el archivo CSV del hospital", type=["csv"])
    
if archivo_subido is not None:
    try:
        st.session_state['data_limpia'] = cd.cargar_y_validar_transacciones(archivo_subido)
    except ValueError as e:
        st.error(f"❌ Error en los datos: {e}")
else:
    st.info("Porfavor sube el archivo CSV")
    

try:
    # Le pasamos el DataFrame limpio que guardamos en session_state
    kpis = cm.calcular_kpis_hospitalarios(st.session_state['data_limpia'])
    
    col1, col2, col3, col4 = st.columns(4)
    # Usamos las claves exactas que le exigimos a Carlos en el README
    col1.metric(label="Volumen total (EUR)", value=f"{kpis['volumen_total_eur']:.2f}%")
    col2.metric(label="Ticket Promedio", value=kpis['ticket_promedio'])
    col3.metric(label="Cantidad de Transacciones", value=kpis['cantidad_transacciones'])

except AttributeError:
    # Si Carlos aún no ha subido su función, mostramos esto:
    st.info("⏳ Esperando el módulo de métricas (Carlos)...")
except Exception as e:
    # Si la función de Carlos tiene un error interno:
    st.error(f"❌ Error en el cálculo de KPIs: {e}")
    
try:
    predicciones = cp.detectar_anomalias(st.session_state['data_limpia'])
    
    # Convertimos la lista en un DataFrame pequeño para graficar
    df_prediccion = pd.DataFrame(predicciones, columns=["Camas Requeridas"])
    df_prediccion.index = range(1, len(predicciones) + 1) 
    
    # Dibujamos el gráfico de barras
    st.bar_chart(df_prediccion)

except AttributeError:
    
    st.info("⏳ Esperando el motor predictivo de demanda (Milán)...")
except Exception as e:
    
    st.error(f"❌ Error al calcular la predicción: {e}")
