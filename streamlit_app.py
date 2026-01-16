import streamlit as st
import pandas as pd
from pathlib import Path
import urllib.parse
import datetime
import requests

# =========================
# Configuración inicial
# =========================

st.set_page_config(
    page_title="Prospección HVAC – SBV",
    page_icon="🧊",
    layout="wide"
)

DATA_PATH = Path("prospectos_hvac.csv")

# =========================
# Funciones base
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
        "Dirección",
        "Rating",
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
    return " ".join([x for x in [keyword, ciudad, estado, pais] if x])


# =========================
# Google Places API
# =========================

def places_text_search(api_key, query):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": api_key,
        "language": "es",
        "region": "mx"
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def places_details(api_key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": api_key,
        "language": "es",
        "fields": "name,formatted_address,formatted_phone_number,website,rating"
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


# =========================
# Session state
# =========================

if "df" not in st.session_state:
    st.session_state.df = cargar_datos()

if "results" not in st.session_state:
    st.session_state.results = []

if "prefill" not in st.session_state:
    st.session_state.prefill = {}

# =========================
# Sidebar
# =========================

st.sidebar.title("🎯 Parámetros de búsqueda")

palabra_clave = st.sidebar.text_input("Palabra clave", "contratista HVAC")

