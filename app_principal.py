import streamlit as st
import pandas as pd

import componente_datos as cd
import componentes_metricas as cm
import componente_prediccion as cp


st.set_page_config(page_title="Analizador de TransAcciones", page_icon="💵", layout="wide")
st.title("💸 Sistema en Tiempo Real de Deteccion de Anomalias en Transacciones")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Configuración")
    archivo_subido = st.file_uploader("Sube el archivo CSV de las transacciones", type=["csv"])
    
if archivo_subido is not None:
    try:
        st.session_state['data_limpia'] = cd.cargar_y_validar_transacciones(archivo_subido)
    except ValueError as e:
        st.error(f"❌ Error en los datos: {e}")
else:
    st.info("Porfavor sube el archivo CSV")
    
if 'data_limpia' in st.session_state:
    df_datos = st.session_state['data_limpia']
    
try:
    # Le pasamos el DataFrame limpio que guardamos en session_state
    kpis = cm.calcular_kpis_fraude(st.session_state['data_limpia'])
    
    col1, col2, col3 = st.columns(3)
    # Usamos las claves exactas que le exigimos a Carlos en el README
    col1.metric(label="Volumen total (EUR)", value=f"{kpis['volumen_total_eur']:.2f}")
    col2.metric(label="Ticket Promedio", value=kpis['ticket_promedio'])
    col3.metric(label="Cantidad de Transacciones", value=kpis['cantidad_transacciones'])

except AttributeError:
    # Si Carlos aún no ha subido su función, mostramos esto:
    st.info("⏳ Esperando el módulo de métricas (Carlos)...")
except Exception as e:
    # Si la función de Carlos tiene un error interno:
    st.error(f"❌ Error en el cálculo de KPIs: {e}")
    
# Detccion de Fraude y Alertas Rojas
try:
        predicciones = cp.detectar_anomalias(df_datos)
        
        if predicciones:
            st.error(f"🚨 **¡ALERTA CRÍTICA DE FRAUDE!** Se detectaron {len(predicciones)} transacción(es) anómala(s).")
            df_anomalias = pd.DataFrame(predicciones)
            st.dataframe(df_anomalias, use_container_width=True)
        else:
            st.success("✅ No se detectó ningún indicador de fraude en las transacciones.")

except AttributeError:
        st.info("⏳ Esperando el motor de detección de anomalías...")
except Exception as e:
        st.error(f"❌ Error al calcular las anomalías: {e}")

st.markdown("---")

    # 3. Gráfico de Barras del Volumen Transaccional
st.subheader("📊 Volumen Transaccional")
try:
        # Preparamos los datos asignando el ID de transacción o fecha como índice
        df_grafico = df_datos.set_index("id_transaccion")[["monto_eur"]]
        st.bar_chart(df_grafico)
except Exception as e:
        st.error(f"❌ Error al generar el gráfico del volumen transaccional: {e}")
