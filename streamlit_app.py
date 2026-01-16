import streamlit as st
import pandas as pd
from pathlib import Path
import urllib.parse
import datetime

# =========================
# CONFIGURACIÓN
# =========================

st.set_page_config(
    page_title="Prospección HVAC – SBV",
    page_icon="🧊",
    layout="wide"
)

DATA_PATH = Path("prospectos_hvac.csv")

# =========================
# FUNCIONES BASE
# =========================

def columnas_base():
    return [
        "Fecha registro",
        "Ciudad",
        "Estado",
        "País",
        "Palabra clave",
        "Tipo cliente",
        "Segmento",
        "Línea producto objetivo",
        "Marca objetivo",
        "Potencial (1-5)",
        "Nombre empresa",
        "Contacto",
        "Cargo",
        "Email",
        "Teléfono",
        "Sitio web",
        "Fuente",
        "Estatus",
        "Próxima acción",
        "Responsable SBV",
        "Notas",
    ]

def cargar_datos():
    cols = columnas_base()
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        for c in cols:
            if c not in df.columns:
                df[c] = ""
        return df[cols]
    return pd.DataFrame(columns=cols)

def guardar_datos(df):
    df.to_csv(DATA_PATH, index=False)

def construir_query(keyword, ciudad, estado, pais):
    partes = [keyword, ciudad, estado, pais]
    partes = [p for p in partes if p]
    return " ".join(partes)

def url_google(query):
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)

def url_maps(query):
    return "https://www.google.com/maps/search/" + urllib.parse.quote_plus(query)

def url_linkedin(query):
    return "https://www.linkedin.com/search/results/companies/?keywords=" + urllib.parse.quote_plus(query)

# =========================
# SESSION STATE
# =========================

if "df" not in st.session_state:
    st.session_state.df = cargar_datos()

df = st.session_state.df

# =========================
# SIDEBAR
# =========================

st.sidebar.title("🎯 Parámetros de búsqueda")

palabra_clave = st.sidebar.text_input("Palabra clave / Giro", "contratista HVAC")
ciudad = st.sidebar.text_input("Ciudad", "Guadalajara")
estado = st.sidebar.text_input("Estado", "Jalisco")
pais = st.sidebar.text_input("País", "México")

query = construir_query(palabra_clave, ciudad, estado, pais)

# =========================
# ENCABEZADO
# =========================

st.title("Prospección de empresas HVAC – SBV Industriales")
st.write("Genera enlaces de búsqueda y captura prospectos sin salir de la app.")

# =========================
# ENLACES DE BÚSQUEDA
# =========================

st.subheader("🔎 Enlaces automáticos")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"[🔎 Buscar en Google]({url_google(query)})", unsafe_allow_html=True)
with col2:
    st.markdown(f"[📍 Buscar en Google Maps]({url_maps(query)})", unsafe_allow_html=True)
with col3:
    st.markdown(f"[💼 Buscar en LinkedIn]({url_linkedin(query)})", unsafe_allow_html=True)

st.caption("Abre los enlaces, encuentra empresas y regístralas abajo.")

st.markdown("---")

# =========================
# FORMULARIO DE PROSPECTO
# =========================

st.subheader("📝 Registrar prospecto")

with st.form("form_prospecto"):

    colA, colB, colC = st.columns(3)

    with colA:
        tipo_cliente = st.selectbox("Tipo cliente", ["Contratista", "Instalador", "Ingeniería", "Usuario final", "Distribuidor"])
    with colB:
        segmento = st.selectbox("Segmento", ["Industrial", "Comercial", "Residencial", "HVACR"])
    with colC:
        linea_producto = st.selectbox("Línea producto", ["Bombas", "Torres", "Filtros", "Controles", "Humidificación", "Ventilación"])

    colD, colE, colF = st.columns(3)
    with colD:
        marca_objetivo = st.selectbox("Marca objetivo", ["Taco", "Lakos", "Honeywell", "Belimo", "Carel", "Evapco", "Greenheck", "Otro"])
    with colE:
        potencial = st.slider("Potencial (1–5)", 1, 5, 3)
    with colF:
        responsable_sbv = st.text_input("Responsable SBV", "Sergio")

    st.markdown("### Datos del prospecto")
    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre de la empresa *")
        contacto = st.text_input("Contacto")
        cargo = st.text_input("Cargo")
        email = st.text_input("Email")
        telefono = st.text_input("Teléfono")
        sitio_web = st.text_input("Sitio web")

    with col2:
        fuente = st.selectbox("Fuente", ["Google", "Google Maps", "LinkedIn", "Referencia", "Otro"])
        estatus = st.selectbox("Estatus", ["Nuevo", "Contactado", "Seguimiento", "Cotización enviada", "Cliente", "Descartado"])
        proxima_accion = st.text_input("Próxima acción", "Llamar / enviar correo")
        notas = st.text_area("Notas")

    submitted = st.form_submit_button("➕ Agregar prospecto")

    if submitted:
        if not nombre:
            st.error("El nombre de la empresa es obligatorio.")
        else:
            nuevo = {
                "Fecha registro": datetime.date.today().isoformat(),
                "Ciudad": ciudad,
                "Estado": estado,
                "País": pais,
                "Palabra clave": palabra_clave,
                "Tipo cliente": tipo_cliente,
                "Segmento": segmento,
                "Línea producto objetivo": linea_producto,
                "Marca objetivo": marca_objetivo,
                "Potencial (1-5)": potencial,
                "Nombre empresa": nombre,
                "Contacto": contacto,
                "Cargo": cargo,
                "Email": email,
                "Teléfono": telefono,
                "Sitio web": sitio_web,
                "Fuente": fuente,
                "Estatus": estatus,
                "Próxima acción": proxima_accion,
                "Responsable SBV": responsable_sbv,
                "Notas": notas,
            }

            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_datos(st.session_state.df)
            st.success(f"Prospecto '{nombre}' guardado.")

# =========================
# TABLA FINAL
# =========================

st.markdown("---")
st.subheader("📋 Prospectos registrados")

st.dataframe(st.session_state.df, use_container_width=True)

csv = st.session_state.df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Descargar CSV", csv, "prospectos_hvac_sbv.csv", "text/csv")

