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
├── app.py                    ← Aplicación principal
├── requirements.txt          ← Dependencias
├── README.md
├── BBDD_PRUEBA_SICETAC.xlsx  ← Base interna SICETAC (DF1)
├── plantilla_tarifax.xlsx    ← Plantilla descargable para usuarios (DF2)
└── logo_header.png           ← Logo del header (opcional)
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
Por defecto el cruce usa `ORIGEN`.  
Cámbiala en la variable `key_col` dentro de la sección TarifaX:
```python
key_col = "ORIGEN"   # ← ajusta al nombre real de tu columna clave
```

### Lógica del merge
Personaliza el tipo de join y transformaciones en `run_merge()`:
```python
def run_merge(df1, df2, key):
    result = pd.merge(df2, df1, on=key, how="right")
    # agrega aquí tus reglas de negocio...
    return result
```

### Columnas de precio para variación
El resultado final incluye automáticamente una columna `variacion_precio` calculada como:

```
variacion_precio = precio_actual (DF2) / precio_sicetac (DF1)
```

Ajusta los nombres exactos de columna en `app.py`:
```python
COL_PRECIO_ACTUAL  = "PRECIO_ACTUAL"    # ← columna de precio del flete actual en DF2
COL_PRECIO_SICETAC = "PRECIO_SICETAC"   # ← columna de precio SICETAC en DF1
```

### Plantilla de carga (DF2)
Para activar el botón de descarga de plantilla en la interfaz, coloca tu archivo en la carpeta del proyecto con el nombre exacto:
```
tarifax/
└── plantilla_tarifax.xlsx   ← tu plantilla aquí
```
El botón aparecerá automáticamente debajo del cargador de archivos con el texto:  
*"Si no tienes la plantilla para cargar el archivo da click aquí para descargarla"*

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

El archivo que el usuario cargue debe contener **al menos** la columna clave y la columna de precio actual:

| ORIGEN    | PRECIO_ACTUAL | ... |
|-----------|---------------|-----|
| BOGOTA    | 150000        | ... |
| MEDELLIN  | 98000         | ... |

> La columna **PRECIO_ACTUAL** se divide entre **PRECIO_SICETAC** (de la base interna) para generar la columna  en el resultado.  
> Si tus columnas tienen nombres distintos, ajusta  y  en .

---

*TarifaX v1.1.0*
