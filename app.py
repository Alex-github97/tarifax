import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io
from datetime import datetime

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="TarifaX",
    page_icon="⚡",
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
    --green-faint: #e8f5eb;
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
    background: var(--charcoal) !important;
    border-right: 1px solid #2e3530;
}
section[data-testid="stSidebar"] * {
    color: #e8f5eb !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    padding: 8px 0;
}

/* ── Sidebar logo area ── */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 20px 0 28px 0;
    border-bottom: 1px solid #3a4a3e;
    margin-bottom: 20px;
}
.sidebar-logo .logo-icon {
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, #369E4D, #5abf6e);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 800;
    color: white;
    font-family: 'Syne', sans-serif;
    letter-spacing: -1px;
    box-shadow: 0 4px 12px rgba(54,158,77,0.4);
}
.sidebar-logo .logo-text {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #ffffff !important;
}
.sidebar-logo .logo-text span {
    color: #5abf6e !important;
}

/* ── Nav items ── */
.nav-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #6b8c72 !important;
    margin-bottom: 8px;
    margin-top: 10px;
}

/* ── Main header ── */
.page-header {
    background: linear-gradient(135deg, var(--green-dark) 0%, var(--green) 60%, var(--green-light) 100%);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 20%;
    width: 240px; height: 240px;
    border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.page-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
    position: relative;
    z-index: 1;
}
.page-header p {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.78);
    margin: 0;
    position: relative;
    z-index: 1;
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
</style>|""", unsafe_allow_html=True)



# ─────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
with st.sidebar:
    # ── Logo corporativo ──────────────────────────────────────
    import os
    from pathlib import Path

    LOGO_NAMES = ["logo icoltrans", "logo icoltrans.png", "logo icoltrans.jpg",
                  "logo icoltrans.jpeg", "logo icoltrans.svg", "logo icoltrans.webp"]
    BASE_DIR   = Path(__file__).parent
    logo_path  = None
    for name in LOGO_NAMES:
        candidate = BASE_DIR / name
        if candidate.exists():
            logo_path = candidate
            break

    if logo_path:
        st.image(str(logo_path), use_container_width=True)
        st.markdown("""
        <div style="text-align:center; margin: -8px 0 20px 0;
                    padding-bottom: 20px; border-bottom: 1px solid #3a4a3e;">
            <span style="font-family:'Syne',sans-serif; font-size:1.3rem;
                         font-weight:800; color:#ffffff; letter-spacing:-0.5px;">
                Tarifa<span style="color:#5abf6e;">X</span>
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sidebar-logo">
            <div class="logo-icon">TX</div>
            <div class="logo-text">Tarifa<span>X</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Navegación</div>', unsafe_allow_html=True)

    nav = st.radio(
        label="Secciones",
        options=["📊  Dashboard", "⚡  TarifaX"],
        label_visibility="collapsed",
    )

    st.markdown('<div style="height:32px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="border-top:1px solid #3a4a3e; padding-top:20px;">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.75rem; color:#6b8c72; line-height:1.7;">
        <strong style="color:#a8c9ae;">TarifaX</strong><br>
        Versión 1.0.0<br>
        {datetime.now().strftime("%d %b %Y")}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SECTION 1 — DASHBOARD POWER BI
# ─────────────────────────────────────────────
if "Dashboard" in nav:
    st.markdown("""
    <div class="page-header">
        <h1>📊 Dashboard TarifaX</h1>
        <p>Panel de control principal · Dashboard de metricas de fletes</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Power BI embed placeholder ──────────────────────────────
    POWERBI_EMBED_URL = "https://app.fabric.microsoft.com/reportEmbed?reportId=ee9e5dd8-ebd1-4656-9b62-90702bec4bca&autoAuth=true&ctid=a4e67291-b9e0-41f5-9be1-356ab2c0918c"   # ← Pega aquí la URL de tu reporte Power BI

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

        # Demo KPIs mientras el PBI no está conectado
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
        st.markdown("#### Métricas de ejemplo")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Tarifas", "12,480", "+3.2%")
        c2.metric("Contratos Activos", "847", "+12")
        c3.metric("Cobertura (%)", "94.7", "+0.5%")
        c4.metric("Última Actualización", "Hoy", "")

        # Demo chart
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
#  SECTION 2 — TARIAFX  (core logic)
# ─────────────────────────────────────────────
elif "TarifaX" in nav:
    st.markdown("""
    <div class="page-header">
        <h1>⚡ TarifaX</h1>
        <p>Motor de cruce de tarifas · Carga tu archivo Excel y obtén el resultado en segundos</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Steps indicator ─────────────────────────────────────────
    st.markdown("""
    <div class="steps">
        <div class="step active"><div class="step-num">1</div> Cargar archivo Excel</div>
        <div class="step active"><div class="step-num">2</div> Cruce automático</div>
        <div class="step active"><div class="step-num">3</div> Descargar resultado</div>
    </div>
    """, unsafe_allow_html=True)

    # ── DF1: base interna (simulada) ─────────────────────────────
    @st.cache_data(show_spinner=False)
    def load_internal_df() -> pd.DataFrame:
        """Simula la carga de la base interna de tarifas (DF1)."""
        np.random.seed(0)
        n = 200
        return pd.DataFrame({
            "origen": [f"PROD-{str(i).zfill(4)}" for i in range(1, n + 1)],
            "destino":  [f"PROD-{str(i).zfill(4)}" for i in range(1, n + 1)],
            "precio":      np.round(np.random.uniform(10, 500, n), 2),
            "tipo_"
            "vehiculo":        np.random.choice(["A", "B", "C", "D"], n),
            "activo":           np.random.choice([True, False], n, p=[0.9, 0.1]),
            "ultima_revision":  pd.date_range("2024-01-01", periods=n, freq="D").strftime("%Y-%m-%d"),
        })

    df_internal = load_internal_df()

    # ── Layout: dos columnas ─────────────────────────────────────
    col_left, col_right = st.columns([1, 1], gap="large")

    # ── LEFT: info base interna ──────────────────────────────────
    with col_left:
        st.markdown("""
        <div class="card">
            <div class="card-title">Tabla de precios</div>
            <div class="card-sub">Datos maestros de tarifas ya cargados en el sistema</div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Registros", f"{len(df_internal):,}")
        m2.metric("Columnas",  len(df_internal.columns))
        m3.metric("Activos",   df_internal["activo"].sum())

        with st.expander("👁️ Vista previa de la tabla de precios", expanded=False):
            st.dataframe(df_internal.head(10), width="stretch", hide_index=True)

    # ── RIGHT: carga de archivo ──────────────────────────────────
    with col_right:
        st.markdown("""
        <div class="card">
            <div class="card-title">Tu Archivo</div>
            <div class="card-sub">Sube el Excel con los datos a cruzar</div>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            label="Arrastra o selecciona tu archivo Excel",
            type=["xlsx", "xls"],
            accept_multiple_files=False,
            help="El archivo debe contener la columna 'codigo_producto' para el cruce.",
        )

        if uploaded_file:
            st.success(f"✅ **{uploaded_file.name}** cargado correctamente")

    # ── MERGE LOGIC ──────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    def run_merge(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """
        Lógica central del merge.
        Modifica aquí el tipo de join, columnas clave, transformaciones,
        reglas de negocio, etc.
        """
        result = pd.merge(
            df2,
            df1,
            on="codigo_producto",
            how="left",
            suffixes=("_externo", "_interno"),
        )
        # Ejemplo de columna calculada
        if "tarifa_base" in result.columns and "cantidad" in result.columns:
            result["total_tarifa"] = result["tarifa_base"] * result["cantidad"]
        result["procesado_en"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return result

    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_excel(uploaded_file)

            st.markdown("""
            <div class="card">
                <div class="card-title">⚙️ Resultado del Merge</div>
                <div class="card-sub">Cruce automático entre la base interna y tu archivo</div>
            </div>
            """, unsafe_allow_html=True)

            key_col = "codigo_producto"

            if key_col not in df_uploaded.columns:
                st.warning(
                    f"⚠️ Tu archivo no contiene la columna clave **`{key_col}`**. "
                    f"Columnas detectadas: `{', '.join(df_uploaded.columns.tolist())}`"
                )
            else:
                df_result = run_merge(df_internal, df_uploaded)

                # KPIs del resultado
                matched    = df_result[key_col].notna().sum() if key_col in df_result else len(df_result)
                unmatched  = len(df_result) - matched
                match_rate = matched / len(df_result) * 100 if len(df_result) else 0

                r1, r2, r3, r4 = st.columns(4)
                r1.metric("Registros resultado",   f"{len(df_result):,}")
                r2.metric("Cruzados correctamente",f"{matched:,}")
                r3.metric("Sin coincidencia",       f"{unmatched:,}")
                r4.metric("Tasa de cruce",          f"{match_rate:.1f}%")

                st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
                st.dataframe(df_result, width="stretch", hide_index=True)

                # ── DOWNLOAD BUTTON ──────────────────────────────
                st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df_result.to_excel(writer, index=False, sheet_name="TarifaX_Resultado")
                output.seek(0)

                filename = f"TarifaX_resultado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

                dl_col, _ = st.columns([1, 2])
                with dl_col:
                    st.download_button(
                        label="⬇️  Descargar Resultado",
                        data=output,
                        file_name=filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {e}")

    else:
        # Placeholder when no file is uploaded
        st.markdown("""
        <div style="background:var(--green-faint); border:2px dashed #a8d5b1;
                    border-radius:14px; padding:48px; text-align:center; color:#6b8c72;">
            <div style="font-size:2.4rem; margin-bottom:10px;">📂</div>
            <strong style="font-family:'Syne',sans-serif; font-size:1rem; color:#1f6130;">
                Sube tu archivo Excel para iniciar el cruce
            </strong>
            <p style="font-size:0.85rem; margin:8px 0 0 0;">
                El resultado estará disponible para descarga inmediatamente después del proceso.
            </p>
        </div>
        """, unsafe_allow_html=True)