import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pathlib import Path
import urllib.parse
import datetime

# Archivo CSV donde se guardará la información
DATA_PATH = Path("prospectos_hvac.csv")

# ---------------------------
# Funciones auxiliares
# ---------------------------

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
        try:
            df = pd.read_csv(DATA_PATH)
            for c in cols:
                if c not in df.columns:
                    df[c] = ""
            df = df[cols]
        except Exception:
            df = pd.DataFrame(columns=cols)
    else:
        df = pd.DataFrame(columns=cols)
    return df


def guardar_datos(df: pd.DataFrame):
    df.to_csv(DATA_PATH, index=False)


def construir_query(keyword: str, ciudad: str, estado: str, pais: str) -> str:
    partes = [keyword.strip(), ciudad.strip(), estado.strip(), pais.strip()]
    partes = [p for p in partes if p]
    return " ".join(partes)


def url_google_search(query: str) -> str:
    return "https://www.google.com/search?q=" + urllib.parse.quote_plus(query)


def url_google_maps(query: str) -> str:
    return "https://www.google.com/maps/search/" + urllib.parse.quote_plus(query)


def url_linkedin_companies(query: str) -> str:
    base = "https://www.linkedin.com/search/results/companies/?keywords="
    return base + urllib.parse.quote_plus(query)


# ---------------------------
# Configuración inicial
# ---------------------------

st.set_page_config(
    page_title="Prospección HVAC – SBV",
    page_icon="🧊",
    layout="wide"
)

if "df" not in st.session_state:
    st.session_state.df = cargar_datos()

df = st.session_state.df

# ---------------------------
# Sidebar – Parámetros de búsqueda
# ---------------------------

st.sidebar.title("🎯 Parámetros de búsqueda")

palabra_clave = st.sidebar.text_input(
    "Palabra clave / Giro",
    value="contratista HVAC"
)

ciudad = st.sidebar.text_input(
    "Ciudad",
    value="Guadalajara"
)

estado = st.sidebar.text_input(
    "Estado",
    value="Jalisco"
)

pais = st.sidebar.text_input(
    "País",
    value="México"
)

st.sidebar.markdown("---")
st.sidebar.write("1) Ajusta ciudad, estado y palabra clave.")
st.sidebar.write("2) Visualiza Google / Maps dentro del app (sin salir).")
st.sidebar.write("3) Captura prospectos abajo.")

# ---------------------------
# Encabezado principal
# ---------------------------

st.title("Prospección de empresas HVAC – SBV Industriales")
st.write(
    "Herramienta para generar búsquedas y registrar prospectos HVAC "
    "por ciudad/estado, enfocada a bombas, torres, filtros, controles y humidificación."
)

# ---------------------------
# Sección: Vista embebida + Captura (sin salir de la ventana)
# ---------------------------

st.subheader("🔍 Búsqueda embebida (sin salir de la app)")

query = construir_query(palabra_clave, ciudad, estado, pais)
google_url = url_google_search(query)
maps_url = url_google_maps(query)

tabs = st.tabs(["🌐 Google", "📍 Google Maps", "💼 LinkedIn (Link)"])

with tabs[0]:
    components.iframe(google_url, height=520, scrolling=True)

with tabs[1]:
    components.iframe(maps_url, height=520, scrolling=True)

with tabs[2]:
    st.warning("LinkedIn normalmente bloquea vista embebida. Usa el link para abrir en otra pestaña.")
    st.markdown(f"[Abrir LinkedIn empresas]({url_linkedin_companies(query)})", unsafe_allow_html=True)

st.caption(
    "Tip: copia nombre/telefono/sitio web desde Google o Maps y pégalo en el formulario. "
    "Luego presiona 'Agregar prospecto'."
)

st.markdown("---")

# ---------------------------
# Registro de prospecto
# ---------------------------

st.subheader("📝 Registrar nuevo prospecto")

with st.form("form_prospecto"):

    st.markdown("### Clasificación comercial SBV")
    col_tc1, col_tc2, col_tc3 = st.columns(3)

    with col_tc1:
        tipo_cliente = st.selectbox(
            "Tipo de cliente",
            ["Contratista", "Instalador", "Ingeniería", "Usuario final", "Distribuidor", "Otro"]
        )

    with col_tc2:
        segmento = st.selectbox(
            "Segmento",
            ["Industrial", "Comercial", "Residencial", "HVACR", "Otro"]
        )

    with col_tc3:
        linea_producto = st.selectbox(
            "Línea producto objetivo",
            ["Bombas", "Torres de enfriamiento", "Filtros / Separadores",
             "Válvulas / Controles", "Humidificación", "Ventilación", "Otro"]
        )

    col_tc4, col_tc5, col_tc6 = st.columns(3)

    with col_tc4:
        marca_objetivo = st.selectbox(
            "Marca objetivo",
            ["Taco", "Lakos", "Honeywell", "Belimo", "Carel", "Dwyer", "Evapco", "Greenheck", "Otra"]
        )

    with col_tc5:
        potencial = st.slider(
            "Potencial (1–5)",
            min_value=1,
            max_value=5,
            value=3
        )

    with col_tc6:
        responsable_sbv = st.text_input("Responsable SBV", value="Sergio")

    st.markdown("### Datos del prospecto")
    col_left, col_right = st.columns(2)

    with col_left:
        nombre_empresa = st.text_input("Nombre de la empresa *")
        contacto = st.text_input("Contacto")
        cargo = st.text_input("Cargo")
        email = st.text_input("Email")
        telefono = st.text_input("Teléfono")
        sitio_web = st.text_input("Sitio web")

    with col_right:
        fuente = st.selectbox("Fuente", ["Google", "Google Maps", "LinkedIn", "Referencia", "Otro"])
        estatus = st.selectbox(
            "Estatus",
            ["Nuevo", "Contactado", "En seguimiento", "Cotización enviada", "Cliente", "Descartado"]
        )
        proxima_accion = st.text_input("Próxima acción", "Llamar / enviar correo / visita")
        notas = st.text_area("Notas", height=120)

    submitted = st.form_submit_button("➕ Agregar prospecto")

    if submitted:
        if not nombre_empresa.strip():
            st.error("El campo 'Nombre de la empresa' es obligatorio.")
        else:
            nueva_fila = {
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
                "Nombre empresa": nombre_empresa.strip(),
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

            st.session_state.df = pd.concat(
                [st.session_state.df, pd.DataFrame([nueva_fila])],
                ignore_index=True
            )
            guardar_datos(st.session_state.df)
            st.success(f"Prospecto '{nombre_empresa.strip()}' agregado correctamente.")

# ---------------------------
# Tabla de prospectos
# ---------------------------

st.markdown("---")
st.subheader("📋 Lista de prospectos registrados")

if st.session_state.df.empty:
    st.info("No hay prospectos registrados aún.")
else:
    st.dataframe(st.session_state.df, use_container_width=True)

    csv_data = st.session_state.df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Descargar CSV",
        csv_data,
        "prospectos_hvac_sbv.csv",
        "text/csv"
    )
