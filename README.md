# ⚡ TarifaX

Aplicación Streamlit para procesamiento y cruce de tarifas.  
Color corporativo: `#369E4D`

---

## 🚀 Instalación rápida

```bash
# 1. Clonar / copiar el proyecto
cd tarifax

# 2. (Opcional) Crear entorno virtual
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
streamlit run app.py
```

La app abre automáticamente en `http://localhost:8501`

---

## 📁 Estructura

```
tarifax/
├── app.py              ← Aplicación principal
├── requirements.txt    ← Dependencias
└── README.md
```

---

## ⚙️ Configuración

### Power BI (Sección 1)
En `app.py`, busca la variable y pega la URL de tu reporte:
```python
POWERBI_EMBED_URL = "https://app.powerbi.com/reportEmbed?reportId=..."
```
Obtenla desde **Power BI Service → Archivo → Publicar en la web → iFrame URL**.

### Base de datos interna (DF1)
En la función `load_internal_df()` reemplaza el DataFrame de prueba con
la conexión real a tu fuente de datos:

```python
# Ejemplo PostgreSQL
import psycopg2
conn = psycopg2.connect("postgresql://user:pass@host/db")
return pd.read_sql("SELECT * FROM tarifas WHERE activo = true", conn)

# Ejemplo archivo local
return pd.read_excel("data/base_interna.xlsx")

# Ejemplo S3 / BigQuery / Snowflake → usa el conector correspondiente
```

### Columna clave del merge
Por defecto el cruce usa `codigo_producto`.  
Cámbiala en la variable `key_col` dentro de la sección TarifaX:
```python
key_col = "codigo_producto"   # ← ajusta al nombre real de tu columna clave
```

### Lógica del merge
Personaliza el tipo de join y transformaciones en `run_merge()`:
```python
def run_merge(df1, df2):
    result = pd.merge(df2, df1, on="codigo_producto", how="left")
    # agrega aquí tus reglas de negocio...
    return result
```

---

## 🔮 Escalabilidad (fases futuras)

| Fase | Tecnología         | Uso previsto                          |
|------|--------------------|---------------------------------------|
| 2    | scikit-learn       | Clasificación / clustering de tarifas |
| 3    | Keras / TensorFlow | Modelos predictivos avanzados         |
| 4    | MLflow / BentoML   | Deployment y versionado de modelos    |

Descomenta las dependencias en `requirements.txt` cuando las necesites.

---

## 📋 Formato esperado del Excel (DF2)

El archivo que el usuario cargue debe contener **al menos** la columna clave:

| codigo_producto | cantidad | ... |
|-----------------|----------|-----|
| PROD-0001       | 5        | ... |
| PROD-0042       | 2        | ... |

---

*TarifaX v1.0.0*
