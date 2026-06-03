import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
import os
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="TarifaX",
    page_icon="logo_header.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── CSS Variables ── */
:root {
    --green:       #369E4D;
    --green-dark:  #1f6130;
    --green-light: #5abf6e;
    --green-faint: #EAF6EA;
    --charcoal:    #1a1f1c;
    --slate:       #2e3530;
    --mist:        #f4f7f5;
    --white:       #ffffff;
    --border:      #d0e4d4;
    --text-main:   #1a1f1c;
    --text-muted:  #6b7c70;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-main);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #EAF6EA !important;
    border-right: 1px solid #c3e6c8;
}
section[data-testid="stSidebar"] * {
    color: #1a1f1c !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    padding: 8px 0;
    color: #1a1f1c !important;
}

/* ── Nav items ── */
.nav-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #369E4D !important;
    margin-bottom: 8px;
    margin-top: 10px;
}

/* ── Main header — degradado EAF6EA ── */
.page-header {
    background: linear-gradient(135deg, #b6deba 0%, #ceefd0 40%, #EAF6EA 100%);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    border: 1px solid #c3e6c8;
}
.page-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(54,158,77,0.08);
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 20%;
    width: 240px; height: 240px;
    border-radius: 50%;
    background: rgba(54,158,77,0.05);
}
.page-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #1f6130;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
    position: relative;
    z-index: 1;
}
.page-header p {
    font-size: 0.95rem;
    color: #3a7a4a;
    margin: 0;
    position: relative;
    z-index: 1;
}

/* ── Header logo image area ── */
.header-logo-area {
    display: flex;
    align-items: center;
    gap: 120px;
    position: relative;
    z-index: 1;
}
.header-logo-area img {
    max-height: 180px;
    object-fit: contain;
}

/* ── Cards ── */
.card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px 28px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--green-dark);
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.card-sub {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin-bottom: 16px;
}

/* ── KPI metric cards ── */
.kpi-row { display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }
.kpi-card {
    flex: 1; min-width: 140px;
    background: var(--white);
    border: 1px solid var(--border);
    border-left: 4px solid var(--green);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.kpi-card .kpi-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}
.kpi-card .kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--green-dark);
    line-height: 1;
}
.kpi-card .kpi-delta {
    font-size: 0.78rem;
    color: var(--green);
    margin-top: 4px;
}

/* ── Upload / action area ── */
.upload-zone {
    background: var(--green-faint);
    border: 2px dashed var(--green-light);
    border-radius: 14px;
    padding: 30px 24px;
    text-align: center;
    margin-bottom: 20px;
}
.upload-zone p { color: var(--text-muted); font-size: 0.88rem; margin: 8px 0 0 0; }

/* ── Status badges ── */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.badge-success { background: #e8f5eb; color: #1f6130; }
.badge-warning { background: #fff8e6; color: #8a6200; }
.badge-info    { background: #e6f4ff; color: #0057a8; }

/* ── Steps indicator ── */
.steps { display: flex; gap: 0; margin-bottom: 28px; }
.step {
    flex: 1;
    padding: 14px 18px;
    background: var(--mist);
    border: 1px solid var(--border);
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text-muted);
    display: flex;
    align-items: center;
    gap: 10px;
}
.step:first-child { border-radius: 10px 0 0 10px; }
.step:last-child  { border-radius: 0 10px 10px 0; }
.step.active {
    background: var(--green);
    color: white;
    border-color: var(--green);
    font-weight: 600;
}
.step .step-num {
    width: 22px; height: 22px;
    border-radius: 50%;
    background: rgba(255,255,255,0.25);
    font-size: 0.75rem;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.step:not(.active) .step-num {
    background: var(--border);
    color: var(--text-muted);
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 24px 0;
}

/* ── Streamlit overrides ── */
.stButton > button {
    background: linear-gradient(135deg, var(--green), var(--green-light)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 14px rgba(54,158,77,0.35) !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(54,158,77,0.45) !important;
}
.stDownloadButton > button {
    background: var(--white) !important;
    color: var(--green-dark) !important;
    border: 2px solid var(--green) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    width: 100%;
}
.stDownloadButton > button:hover {
    background: var(--green-faint) !important;
}
div[data-testid="stFileUploader"] {
    background: var(--green-faint);
    border: 2px dashed var(--green-light);
    border-radius: 14px;
    padding: 10px;
}
.stDataFrame { border-radius: 10px; overflow: hidden; }
[data-testid="stMetric"] {
    background: var(--white);
    border: 1px solid var(--border);
    border-left: 4px solid var(--green);
    border-radius: 12px;
    padding: 14px 18px;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    color: var(--green-dark) !important;
    font-size: 1.6rem !important;
}
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 0.78rem !important; }
.stSuccess { border-radius: 10px !important; }
.stInfo    { border-radius: 10px !important; }
.stWarning { border-radius: 10px !important; }

/* ── Sidebar toggle: siempre visible ── */
button[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    visibility: visible !important;
    opacity: 1 !important;
    display: flex !important;
    background: var(--green) !important;
    border-radius: 0 8px 8px 0 !important;
    color: white !important;
    z-index: 9999 !important;
}
button[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapsedControl"] svg {
    fill: white !important;
    stroke: white !important;
}
</style>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    # ── Logo corporativo en sidebar ───────────────────────────
    LOGO_NAMES = ["logo icoltrans.png", "logo icoltrans.jpg",
                  "logo icoltrans.jpeg", "logo icoltrans.svg",
                  "logo icoltrans.webp", "logo icoltrans"]
    BASE_DIR  = Path(__file__).parent
    logo_path = None
    for name in LOGO_NAMES:
        candidate = BASE_DIR / name
        if candidate.exists():
            logo_path = candidate
            break

    if logo_path:
        st.image(str(logo_path), use_container_width=True)
    else:
        # Fallback: ícono sin texto TarifaX
        st.markdown("""
        <div style="display:flex; justify-content:center; padding: 20px 0 16px 0;
                    border-bottom: 1px solid #c3e6c8; margin-bottom: 16px;">
            <div style="width:48px; height:48px;
                        background: linear-gradient(135deg, #369E4D, #5abf6e);
                        border-radius: 12px; display:flex; align-items:center;
                        justify-content:center; font-family:'Syne',sans-serif;
                        font-size:1.1rem; font-weight:800; color:white;
                        box-shadow: 0 4px 12px rgba(54,158,77,0.3);">TX</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-label">Navegación</div>', unsafe_allow_html=True)

    nav = st.radio(
        label="Secciones",
        options=["📊  Dashboard", "⚡  TarifaX"],
        label_visibility="collapsed",
    )

    st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="border-top:1px solid #c3e6c8; padding-top:20px;">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.75rem; color:#4a7a54; line-height:1.7;">
        <strong style="color:#1f6130;">TarifaX</strong><br>
        Versión 1.0.0<br>
        {datetime.now().strftime("%d %b %Y")}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SECTION 1 — DASHBOARD POWER BI
# ─────────────────────────────────────────────
if "Dashboard" in nav:

    # ── Header con imagen de logo ────────────────────────────────
    # INSTRUCCIÓN: Para mostrar tu logo en el header del Dashboard,
    # guarda la imagen como "logo_header.png" (o .jpg/.svg/.webp)
    # en la misma carpeta que este archivo app.py.
    # Si no existe, se muestra el título en texto.

    HEADER_LOGO_NAMES = ["logo_header.png", "logo_header.jpg",
                         "logo_header.jpeg", "logo_header.svg", "logo_header.webp"]
    header_logo_path = None
    for name in HEADER_LOGO_NAMES:
        candidate = BASE_DIR / name
        if candidate.exists():
            header_logo_path = candidate
            break

    if header_logo_path:
        import base64
        with open(header_logo_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        ext = Path(header_logo_path).suffix.lstrip(".")
        mime = "image/svg+xml" if ext == "svg" else f"image/{ext}"
        st.markdown(f"""
        <div class="page-header">
            <div class="header-logo-area">
                <img src="data:{mime};base64,{img_b64}" alt="Logo TarifaX" />
                <p>Panel de control principal · Dashboard de métricas de fletes</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="page-header">
            <h1>📊 Dashboard TarifaX</h1>
            <p>Panel de control principal · Dashboard de métricas de fletes</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Power BI embed ───────────────────────────────────────────
    POWERBI_EMBED_URL = "https://app.powerbi.com/view?r=eyJrIjoiNTA3OGUwYjMtYzFiNC00MGI1LWFiODctMmJhNWJhNGJmYTVlIiwidCI6ImE0ZTY3MjkxLWI5ZTAtNDFmNS05YmUxLTM1NmFiMmMwOTE4YyIsImMiOjR9"

    if POWERBI_EMBED_URL:
        st.components.v1.iframe(POWERBI_EMBED_URL, height=600, scrolling=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding:60px 40px;">
            <div style="font-size:3rem; margin-bottom:12px;">📈</div>
            <div class="card-title" style="font-size:1.1rem; justify-content:center;">Power BI · Pendiente de configuración</div>
            <p style="color:var(--text-muted); font-size:0.88rem; margin:10px 0 0 0;">
                Edita la variable <code>POWERBI_EMBED_URL</code> en <strong>app.py</strong> con la URL de publicación de tu reporte.<br>
                Puedes obtenerla desde <em>Power BI Service → Archivo → Publicar en la web</em>.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown("#### Métricas de ejemplo")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Tarifas", "12,480", "+3.2%")
        c2.metric("Contratos Activos", "847", "+12")
        c3.metric("Cobertura (%)", "94.7", "+0.5%")
        c4.metric("Última Actualización", "Hoy", "")

        np.random.seed(42)
        months = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
        df_demo = pd.DataFrame({
            "Mes": months,
            "Tarifas Procesadas": np.random.randint(900, 1200, 12),
            "Contratos Nuevos":   np.random.randint(50, 130, 12),
        })
        fig = px.bar(
            df_demo, x="Mes", y="Tarifas Procesadas",
            color_discrete_sequence=["#369E4D"],
            title="Tarifas procesadas por mes (demo)",
        )
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font_family="DM Sans",
            title_font_family="Syne",
            title_font_size=14,
            showlegend=False,
        )
        fig.update_traces(marker_line_width=0, marker_line_color="white")
        st.plotly_chart(fig, width="stretch")


# ─────────────────────────────────────────────
#  SECTION 2 — TARIAFX  (motor de merge)
# ─────────────────────────────────────────────
elif "TarifaX" in nav:

    # ── Header con imagen de logo ────────────────────────────────
    # INSTRUCCIÓN: Misma imagen "logo_header.png" (o .jpg/.svg/.webp)
    # en la carpeta del proyecto. Si no existe, se usa título en texto.

    HEADER_LOGO_NAMES = ["logo_header.png", "logo_header.jpg",
                         "logo_header.jpeg", "logo_header.svg", "logo_header.webp"]
    header_logo_path = None
    for name in HEADER_LOGO_NAMES:
        candidate = BASE_DIR / name
        if candidate.exists():
            header_logo_path = candidate
            break

    if header_logo_path:
        import base64
        with open(header_logo_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        ext = Path(header_logo_path).suffix.lstrip(".")
        mime = "image/svg+xml" if ext == "svg" else f"image/{ext}"
        st.markdown(f"""
        <div class="page-header">
            <div class="header-logo-area">
                <img src="data:{mime};base64,{img_b64}" alt="Logo TarifaX" />
                <p>Motor de cruce de tarifas · Carga tu archivo Excel y obtén el resultado en segundos</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="page-header">
            <h1>⚡ TarifaX</h1>
            <p>Motor de cruce de tarifas · Carga tu archivo Excel y obtén el resultado en segundos</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Steps indicator ──────────────────────────────────────────
    st.markdown("""
    <div class="steps">
        <div class="step active"><div class="step-num">1</div> Cargar archivo Excel</div>
        <div class="step active"><div class="step-num">2</div> Cruce automático</div>
        <div class="step active"><div class="step-num">3</div> Descargar resultado</div>
    </div>
    """, unsafe_allow_html=True)

    # ────────────────────────────────────────────────────────────
    #  DF1 — BASE INTERNA (cargada directamente con pd.read_excel)
    #
    #  INSTRUCCIÓN: Reemplaza la ruta de abajo con la ruta real
    #  de tu archivo Excel interno, por ejemplo:
    #      DF1_PATH = BASE_DIR / "data" / "tarifas_internas.xlsx"
    #  o una ruta absoluta:
    #      DF1_PATH = Path("C:/datos/base_interna.xlsx")
    # ────────────────────────────────────────────────────────────
    DF1_PATH = BASE_DIR / "BBDD_PRUEBA_SICETAC.xlsx"   # ← AJUSTA ESTA RUTA

    @st.cache_data(show_spinner=False)
    def load_internal_df(path: str) -> pd.DataFrame:
        return pd.read_excel(path)

    # ── Layout: dos columnas ─────────────────────────────────────
    col_left, col_right = st.columns([1, 1], gap="large")

    # ── LEFT: base interna (DF1) ─────────────────────────────────
    with col_left:
        st.markdown("""
        <div class="card">
            <div class="card-title">Base Interna (DF1)</div>
            <div class="card-sub">Datos maestros cargados desde el archivo Excel interno</div>
        </div>
        """, unsafe_allow_html=True)

        if DF1_PATH.exists():
            try:
                df_internal = load_internal_df(str(DF1_PATH))
                m1, m2 = st.columns(2)
                m1.metric("Registros", f"{len(df_internal):,}")
                m2.metric("Columnas",  len(df_internal.columns))
                with st.expander("👁️ Vista previa — Base interna", expanded=False):
                    st.dataframe(df_internal.head(10), use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f"❌ No se pudo cargar **{DF1_PATH.name}**: {e}")
                df_internal = None
        else:
            st.warning(
                f"⚠️ Archivo interno no encontrado: `{DF1_PATH}`\n\n"
                "Ajusta la variable `DF1_PATH` en el código con la ruta correcta."
            )
            df_internal = None

    # ── RIGHT: carga de archivo del usuario (DF2) ────────────────
    with col_right:
        st.markdown("""
        <div class="card">
            <div class="card-title">Tu Archivo (DF2)</div>
            <div class="card-sub">Sube el Excel con los datos a cruzar contra la base interna</div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            label="Arrastra o selecciona tu archivo Excel",
            type=["xlsx", "xls"],
            accept_multiple_files=False,
            help="Sube el archivo Excel que deseas cruzar con la base interna.",
        )

        if uploaded_file:
            st.success(f"✅ **{uploaded_file.name}** cargado correctamente")

    # ────────────────────────────────────────────────────────────
    #  MERGE LOGIC
    #
    #  INSTRUCCIÓN: Ajusta la variable key_col con el nombre exacto
    #  de la columna que se usará como llave del cruce entre DF1 y DF2.
    #  También puedes personalizar el tipo de join (how=) y agregar
    #  columnas calculadas o reglas de negocio dentro de run_merge().
    # ────────────────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    key_col = "ORIGEN"   # ← AJUSTA AL NOMBRE REAL DE TU COLUMNA CLAVE

    def run_merge(df1: pd.DataFrame, df2: pd.DataFrame, key: str) -> pd.DataFrame:
        """
        Lógica central del merge entre DF1 (base interna) y DF2 (archivo cargado).
        Modifica aquí el tipo de join, sufijos, columnas calculadas y
        reglas de negocio según tus necesidades.
        """
        result = pd.merge(
            df2,
            df1,
            on=key,
            how="right",
            suffixes=("_externo", "_interno"),
        )
        result["procesado_en"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return result

    if uploaded_file is not None and df_internal is not None:
        try:
            df_uploaded = pd.read_excel(uploaded_file)

            st.markdown("""
            <div class="card">
                <div class="card-title">⚙️ Resultado del Merge</div>
                <div class="card-sub">Cruce entre la base interna (DF1) y tu archivo (DF2)</div>
            </div>
            """, unsafe_allow_html=True)

            if key_col not in df_uploaded.columns or key_col not in df_internal.columns:
                missing_in = []
                if key_col not in df_uploaded.columns:
                    missing_in.append(f"DF2 — columnas disponibles: `{', '.join(df_uploaded.columns.tolist())}`")
                if key_col not in df_internal.columns:
                    missing_in.append(f"DF1 — columnas disponibles: `{', '.join(df_internal.columns.tolist())}`")
                st.warning(
                    f"⚠️ La columna clave **`{key_col}`** no se encontró en:\n\n" +
                    "\n".join(f"- {m}" for m in missing_in) +
                    f"\n\nAjusta la variable `key_col` en el código."
                )
            else:
                df_result = run_merge(df_internal, df_uploaded, key_col)

                matched    = df_result[key_col].notna().sum()
                unmatched  = len(df_result) - matched
                match_rate = matched / len(df_result) * 100 if len(df_result) else 0

                r1, r2, r3, r4 = st.columns(4)
                r1.metric("Registros resultado",    f"{len(df_result):,}")
                r2.metric("Cruzados correctamente", f"{matched:,}")
                r3.metric("Sin coincidencia",       f"{unmatched:,}")
                r4.metric("Tasa de cruce",          f"{match_rate:.1f}%")

                st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
                st.dataframe(df_result, use_container_width=True, hide_index=True)

                # ── DOWNLOAD BUTTON ──────────────────────────────
                st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df_result.to_excel(writer, index=False, sheet_name="TarifaX_Resultado")
                output.seek(0)

                filename = f"TarifaX_resultado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

                dl_col, _ = st.columns([1, 2])
                with dl_col:
                    st.download_button(
                        label="⬇️  Descargar archivo",
                        data=output,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {e}")

    elif uploaded_file is None:
        st.markdown("""
        <div style="background:#EAF6EA; border:2px dashed #a8d5b1;
                    border-radius:14px; padding:48px; text-align:center; color:#4a7a54;">
            <div style="font-size:2.4rem; margin-bottom:10px;">📂</div>
            <strong style="font-family:'Syne',sans-serif; font-size:1rem; color:#1f6130;">
                Sube tu archivo Excel (DF2) para iniciar el cruce
            </strong>
            <p style="font-size:0.85rem; margin:8px 0 0 0;">
                El resultado estará disponible para descarga inmediatamente después del proceso.
            </p>
        </div>
        """, unsafe_allow_html=True)
