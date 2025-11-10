================================================================================
🚖 NYC TAXI - ANÁLISIS GEOESPACIAL DE MOVILIDAD URBANA
================================================================================

RESUMEN EJECUTIVO
--------------------------------------------------------------------------------
Sistema de análisis geoespacial que procesa datos de taxis de Nueva York para 
visualizar patrones de movilidad urbana mediante dashboards interactivos con 
mapas de calor y flujos de viaje.

Tecnologías: Python | FastAPI | Streamlit | PyDeck | Pandas
Grupo 9: Leonardo Mafla • Vanessa Nasimba • Edwin Tapia • Sebastian Morales

================================================================================
TABLA DE CONTENIDOS
================================================================================
1. INSTALACIÓN Y CONFIGURACIÓN
2. EJECUCIÓN DE LA APLICACIÓN
3. USO DEL DASHBOARD
4. ARQUITECTURA DEL SISTEMA
5. API REST - ENDPOINTS
6. SOLUCIÓN DE PROBLEMAS

================================================================================
1. INSTALACIÓN Y CONFIGURACIÓN
================================================================================

PASO 1: VERIFICAR REQUISITOS PREVIOS
--------------------------------------------------------------------------------
Requisitos mínimos:
✅ Python 3.8 - 3.11 (recomendado 3.10)
✅ pip 21.0+
✅ Git 2.0+
✅ 4GB RAM mínimo
✅ 5GB espacio en disco

Verificar instalaciones:
    python --version
    pip --version
    git --version

Salida esperada:
    Python 3.10.x
    pip 23.x.x
    git version 2.x.x

PASO 2: CLONAR EL REPOSITORIO
--------------------------------------------------------------------------------
Comandos:
    git clone https://github.com/tu-usuario/Grupo9_MovilidadUrbanaCaso.git
    cd Grupo9_MovilidadUrbanaCaso

PASO 3: CREAR ENTORNO VIRTUAL
--------------------------------------------------------------------------------
En Windows:
    python -m venv venv
    venv\Scripts\activate

En Linux/Mac:
    python3 -m venv venv
    source venv/bin/activate

Verificación exitosa:
    El prompt debe mostrar (venv) al inicio:
    (venv) C:\Users\usuario\Grupo9_MovilidadUrbanaCaso>

PASO 4: INSTALAR DEPENDENCIAS
--------------------------------------------------------------------------------
Comandos:
    pip install --upgrade pip
    pip install -r requirements.txt

Este proceso instalará:
    - pandas==2.3.3
    - fastapi==0.121.0
    - streamlit==1.51.0
    - pydeck==0.9.1
    - plotly==6.3.1
    - uvicorn==0.38.0
    - pyarrow==21.0.0
    - requests==2.32.5
    - Y otras dependencias...

Verificar instalación:
    pip show pandas fastapi streamlit

Tiempo estimado: 3-5 minutos

PASO 5: DESCARGAR EL DATASET
--------------------------------------------------------------------------------
OPCIÓN A - Descarga Manual:
1. Visitar: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
2. Buscar: Yellow Taxi Trip Records - January 2015
3. Descargar el archivo
4. Renombrar a: yellow_tripdata_2015-01.csv
5. Colocar en la carpeta: data/

OPCIÓN B - Descarga con Comando (Linux/Mac):
    mkdir -p data
    curl -o data/yellow_tripdata_2015-01.csv \
      https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2015-01.parquet

Verificar descarga:
    # Windows
    dir data\yellow_tripdata_2015-01.csv
    
    # Linux/Mac
    ls -lh data/yellow_tripdata_2015-01.csv

Tamaño esperado: ~1.8 GB

⚠️ IMPORTANTE: El archivo es grande, la descarga puede tomar varios minutos

PASO 6: PROCESAR LOS DATOS
--------------------------------------------------------------------------------
Comando:
    python main.py

Salida esperada:
    Ejecutando el script desde: C:\...\main.py
    Cargando datos desde: C:\...\data\yellow_tripdata_2015-01.csv
    Datos cargados exitosamente.
    Iniciando el proceso de limpieza de datos...
    Limpiando los nombres de las columnas...
    Convirtiendo columnas de fechas a tipo datetime...
    Eliminando filas con coordenadas inválidas...
    Filtrando filas fuera del rango geográfico de NY válido...
    Eliminando columnas innecesarias...
    Redondear las coordenadas con 4 decimales
    
    ---LIMPIEZA DE DATOS TERMINADO---
    
    ---INICIANDO IMPUTACIÓN DE DATOS---
    Rellenando valores de 'passengers' que son cero con la mediana...
    eliminar valores en na de las coordenadas
    Registros después de limpieza: 10,906,858
    
    ---IMPUTACIÓN DE DATOS TERMINADO---
    
    ---INICIANDO AGREGACIÓN NUEVAS COLUMNAS---
    Creando la columna 'pickup_hour'...
    Creando la columna 'dropoff_hour'...
    Creando la columna 'pickup_day_of_week'...
    Creando la columna 'pickup_date'...
    Creando la columna 'dropoff_date'...
    Creando la columna 'trip_duration'...
    Creando la columna 'is_peak_hour'...
    Asignando zonas pickup de viaje según coordenadas...
    Asignando zonas dropoff de viaje según coordenadas...
    
    ---AGREGACIÓN NUEVAS COLUMNAS TERMINADO---
    
    Guardando el DataFrame limpio en: ...\data\processed\tripdata_cleaned.csv
    Archivo guardado exitosamente.
    
    ---PIPELINE TERMINADO---

Resultado:
    ✅ Archivo creado: data/processed/tripdata_cleaned.csv
    ✅ Tiempo de procesamiento: 5-10 minutos

================================================================================
2. EJECUCIÓN DE LA APLICACIÓN
================================================================================

⚠️ IMPORTANTE: NECESITAS DOS TERMINALES ABIERTAS SIMULTÁNEAMENTE

TERMINAL 1: INICIAR LA API
--------------------------------------------------------------------------------
Paso 1 - Preparar Terminal 1:
    cd Grupo9_MovilidadUrbanaCaso
    
    # Activar entorno virtual
    # Windows:
    venv\Scripts\activate
    
    # Linux/Mac:
    source venv/bin/activate

Paso 2 - Iniciar API:
    uvicorn api_app:app --host 0.0.0.0 --port 8000 --reload

Salida esperada:
    INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
    INFO: Started reloader process [12345]
    INFO: Started server process [12346]
    INFO: Application startup complete.

Verificar que funciona:
    Abrir navegador: http://localhost:8000/docs
    Deberías ver la documentación de Swagger UI

⚠️ NO CIERRES ESTA TERMINAL - Debe permanecer abierta

TERMINAL 2: INICIAR EL DASHBOARD
--------------------------------------------------------------------------------
Paso 1 - Abrir NUEVA Terminal:
    cd Grupo9_MovilidadUrbanaCaso
    
    # Activar entorno virtual
    # Windows:
    venv\Scripts\activate
    
    # Linux/Mac:
    source venv/bin/activate

Paso 2 - Iniciar Dashboard:
    streamlit run dashboard.py

Salida esperada:
    You can now view your Streamlit app in your browser.
    Local URL: http://localhost:8501
    Network URL: http://192.168.X.X:8501

Resultado:
    ✅ El navegador se abre automáticamente en http://localhost:8501
    ✅ Verás el dashboard con el título:
       "🚖 Dashboard de Análisis Geoespacial - NYC Yellow Taxi"

⚠️ NO CIERRES ESTA TERMINAL - Debe permanecer abierta

ESTADO FINAL
--------------------------------------------------------------------------------
Terminal 1 (API):
    (venv) uvicorn api_app:app --host 0.0.0.0 --port 8000 --reload
    INFO: Uvicorn running on http://0.0.0.0:8000
    [Ejecutándose - NO CERRAR]

Terminal 2 (Dashboard):
    (venv) streamlit run dashboard.py
    Local URL: http://localhost:8501
    [Ejecutándose - NO CERRAR]

Para detener: Presiona CTRL+C en cada terminal cuando termines

================================================================================
3. USO DEL DASHBOARD
================================================================================

INTERFAZ PRINCIPAL
--------------------------------------------------------------------------------
El dashboard se divide en tres secciones:

1. PANEL SUPERIOR - KPIs (Indicadores Clave)
   
   📈 Total de Viajes - Cantidad total en el período seleccionado
   📏 Distancia Promedio (mi) - Distancia media en millas
   ⏱️ Duración Promedio (min) - Tiempo promedio en minutos
   👥 Pasajeros Promedio - Ocupación media por viaje

2. SIDEBAR IZQUIERDO - Filtros de Control
   
   📊 Filtros para KPI:
   • Rango de fechas: 01/01/2015 - 31/01/2015
   • Hora del día: Slider 0-23 (por defecto: 8)
   • Número de pasajeros: Rango 1-6 (por defecto: 1-4)
   
   🗺️ Filtros para Mapas:
   • Zona de Origen: 
     - Todas
     - JFK Airport
     - LaGuardia Airport
     - Downtown Manhattan
     - Times Square
     - Grand Central Terminal
     - Penn Station
     - Otra zona

3. TABS DE VISUALIZACIÓN
   
   Tab 1: 🔥 Mapa de Calor origen
   - Visualiza puntos de recogida (pickup)
   - Muestra densidad de demanda
   - Filtrado por hora seleccionada
   - Máximo 20,000 puntos
   
   Tab 2: 🔥 Mapa de Calor destino
   - Visualiza puntos de destino (dropoff)
   - Identifica áreas de alta llegada
   - Filtrado por hora seleccionada
   - Máximo 20,000 puntos
   
   Tab 3: 🧭 Mapa de Flujos
   - Muestra rutas origen-destino
   - Arcos visuales entre puntos
   - Filtrado por zona de origen
   - Máximo 1,000 flujos por zona

EJEMPLO DE USO
--------------------------------------------------------------------------------
Caso: Analizar tráfico desde Times Square en hora pico matutina

Paso 1 - Configurar Filtros:
    1. Ir al Sidebar (panel izquierdo)
    2. Seleccionar fechas: 01/01/2015 - 15/01/2015
    3. Ajustar hora: 8 (8:00 AM)
    4. Pasajeros: 1 a 4
    5. Zona: "Times Square"

Paso 2 - Observar KPIs:
    Total de Viajes: 1,234
    Distancia Promedio: 3.45 mi
    Duración Promedio: 15.2 min
    Pasajeros Promedio: 1.8

Paso 3 - Analizar Visualizaciones:
    Tab 1: Ver zonas rojas (alta densidad de recogidas)
    Tab 2: Ver destinos más frecuentes
    Tab 3: Ver arcos desde Times Square

Paso 4 - Interpretar Resultados:
    ✓ Identificar zonas de alta demanda
    ✓ Detectar patrones de movilidad
    ✓ Optimizar distribución de taxis

FUNCIONALIDADES INTERACTIVAS
--------------------------------------------------------------------------------
Mapas:
    • Zoom: Scroll del mouse
    • Pan: Click y arrastrar
    • Rotación: Click derecho y arrastrar
    • Reset: Doble click

Actualización:
    • Los filtros actualizan automáticamente los KPIs
    • Tiempo de carga: 2-5 segundos

================================================================================
4. ARQUITECTURA DEL SISTEMA
================================================================================

ESTRUCTURA DEL PROYECTO
--------------------------------------------------------------------------------
Grupo9_MovilidadUrbanaCaso/
│
├── README.md                   # Documentación completa
├── requirements.txt            # Dependencias Python
├── .gitignore                  # Archivos ignorados
│
├── data/
│   ├── yellow_tripdata_2015-01.csv    # Dataset original (1.8 GB)
│   └── processed/
│       └── tripdata_cleaned.csv        # Dataset procesado (~800 MB)
│
├── scripts/
│   ├── data_loader.py          # Carga de datos
│   ├── data_cleaning.py        # Limpieza
│   ├── data_imputation.py      # Imputación
│   ├── data_new_features.py    # Nuevas características
│   └── data_saving.py          # Guardado
│
├── main.py                     # Pipeline de procesamiento
├── api_app.py                  # API REST (FastAPI)
└── dashboard.py                # Dashboard (Streamlit)

FLUJO DE DATOS
--------------------------------------------------------------------------------
📥 DATOS CRUDOS (12M+ registros)
   └─ data/yellow_tripdata_2015-01.csv
         ↓
🧹 LIMPIEZA (data_cleaning.py)
   • Normalizar nombres de columnas
   • Convertir tipos de datos (fechas)
   • Eliminar coordenadas (0,0)
   • Filtro geográfico NYC (40.5-41.0°N, -74.3--73.6°W)
   • Eliminar columnas innecesarias
   • Redondear coordenadas (4 decimales)
         ↓
🔄 IMPUTACIÓN (data_imputation.py)
   • Rellenar pasajeros=0 con mediana
   • Eliminar coordenadas nulas
         ↓
✨ NUEVAS CARACTERÍSTICAS (data_new_features.py)
   • pickup_hour, dropoff_hour
   • pickup_day_of_week
   • pickup_date, dropoff_date
   • trip_duration (minutos)
   • is_peak_hour (7-9 AM, 5-7 PM)
   • pickup_zone, dropoff_zone
         ↓
💾 DATOS PROCESADOS (~10M registros válidos)
   └─ data/processed/tripdata_cleaned.csv
         ↓
🚀 API REST (FastAPI - Puerto 8000)
   • /filters/options
   • /options/kpi
   • /heatmap/pickup
   • /heatmap/dropoff
   • /flow
         ↓
📊 DASHBOARD INTERACTIVO (Streamlit - Puerto 8501)
   • Filtros dinámicos
   • KPIs en tiempo real
   • Mapas de calor (PyDeck)
   • Visualización de flujos

COLUMNAS DEL DATASET PROCESADO
--------------------------------------------------------------------------------
Columna                 Tipo         Descripción
----------------------  -----------  ------------------------------------------
pickup_datetime         datetime64   Fecha y hora de recogida
dropoff_datetime        datetime64   Fecha y hora de llegada
passengers              int64        Número de pasajeros
distance                float64      Distancia del viaje (millas)
fare_amount             float64      Tarifa del viaje
total_amount            float64      Monto total pagado
pickup_longitude        float64      Longitud de recogida
pickup_latitude         float64      Latitud de recogida
dropoff_longitude       float64      Longitud de destino
dropoff_latitude        float64      Latitud de destino
pickup_hour             int64        Hora de recogida (0-23)
dropoff_hour            int64        Hora de llegada (0-23)
pickup_day_of_week      object       Día de la semana
pickup_date             datetime64   Fecha de recogida
dropoff_date            datetime64   Fecha de llegada
trip_duration           float64      Duración del viaje (minutos)
is_peak_hour            bool         Indicador de hora pico
pickup_zone             object       Zona de recogida
dropoff_zone            object       Zona de destino

ZONAS GEOGRÁFICAS IDENTIFICADAS
--------------------------------------------------------------------------------
✈️ JFK Airport              (40.63-40.65°N, -73.79--73.76°W)
✈️ LaGuardia Airport        (40.76-40.78°N, -73.89--73.86°W)
🏙️ Downtown Manhattan       (40.70-40.72°N, -74.02--74.00°W)
🎭 Times Square             (40.755-40.76°N, -73.99--73.98°W)
🚉 Grand Central Terminal   (40.750-40.753°N, -73.979--73.974°W)
🚉 Penn Station             (40.748-40.752°N, -73.996--73.990°W)
📍 Otras zonas              (resto de NYC)

================================================================================
5. API REST - ENDPOINTS
================================================================================

BASE URL: http://localhost:8000

DOCUMENTACIÓN INTERACTIVA
--------------------------------------------------------------------------------
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

ENDPOINT 1: OPCIONES DE FILTROS
--------------------------------------------------------------------------------
GET /filters/options

Descripción:
    Devuelve las opciones disponibles para construir los filtros del dashboard:
    rango de fechas, horas, pasajeros y zonas.

Respuesta:
{
  "fecha_min": "2015-01-01",
  "fecha_max": "2015-01-31",
  "hora_min": 0,
  "hora_max": 23,
  "pass_min": 1,
  "pass_max": 6,
  "zonas_disponibles": [
    "Todas",
    "JFK Airport",
    "LaGuardia Airport",
    "Downtown Manhattan",
    "Times Square",
    "Grand Central Terminal",
    "Penn Station",
    "Otra zona"
  ]
}

ENDPOINT 2: INDICADORES KPI
--------------------------------------------------------------------------------
GET /options/kpi

Parámetros:
    start_date (string)  - Fecha inicial (YYYY-MM-DD)
    end_date (string)    - Fecha final (YYYY-MM-DD)
    hour (integer)       - Hora del día (0-23)
    pass_min (integer)   - Cantidad mínima de pasajeros
    pass_max (integer)   - Cantidad máxima de pasajeros

Ejemplo:
GET /options/kpi?start_date=2015-01-01&end_date=2015-01-15&hour=8&pass_min=1&pass_max=4

Respuesta:
{
  "message": "✅ 45,678 viajes encontrados.",
  "total_viajes": 45678,
  "promedio_distancia": 3.45,
  "duracion_promedio": 15.2,
  "pasajeros_promedio": 1.8
}

ENDPOINT 3: MAPA DE CALOR - ORIGEN
--------------------------------------------------------------------------------
GET /heatmap/pickup

Parámetros:
    start_date (string)  - Fecha inicial (YYYY-MM-DD)
    end_date (string)    - Fecha final (YYYY-MM-DD)
    hour (integer)       - Hora específica (0-23) [opcional]

Ejemplo:
GET /heatmap/pickup?start_date=2015-01-01&end_date=2015-01-15&hour=8

Respuesta:
{
  "message": "✅ 20,000 puntos generados para el mapa de calor.",
  "count": 20000,
  "data": [
    {
      "lat": 40.7589,
      "lon": -73.9851,
      "pickup_hour": 8,
      "pickup_date": "2015-01-15"
    },
    ...
  ]
}

Nota: Máximo 20,000 puntos para optimizar rendimiento

ENDPOINT 4: MAPA DE CALOR - DESTINO
--------------------------------------------------------------------------------
GET /heatmap/dropoff

Parámetros:
    start_date (string)  - Fecha inicial (YYYY-MM-DD)
    end_date (string)    - Fecha final (YYYY-MM-DD)
    hour (integer)       - Hora específica (0-23) [opcional]

Ejemplo:
GET /heatmap/dropoff?start_date=2015-01-01&end_date=2015-01-15&hour=8

Respuesta:
{
  "message": "✅ 20,000 puntos generados para el mapa de calor.",
  "count": 20000,
  "data": [
    {
      "lat": 40.7128,
      "lon": -74.0060,
      "dropoff_hour": 8,
      "dropoff_date": "2015-01-15"
    },
    ...
  ]
}

ENDPOINT 5: FLUJOS POR ZONA
--------------------------------------------------------------------------------
GET /flow

Parámetros:
    zona (string)    - Nombre de la zona de origen
    limite (integer) - Número máximo de flujos (100-5000, default: 1000)

Ejemplo:
GET /flow?zona=Times Square&limite=1000

Respuesta:
{
  "message": "✅ 1,000 flujos obtenidos desde la zona 'Times Square'.",
  "count": 1000,
  "zone": "Times Square",
  "data": [
    {
      "lat_origen": 40.7589,
      "lon_origen": -73.9851,
      "lat_destino": 40.7128,
      "lon_destino": -74.0060
    },
    ...
  ]
}

CÓDIGOS DE RESPUESTA
--------------------------------------------------------------------------------
200 - OK: Solicitud exitosa
400 - Bad Request: Parámetros inválidos
404 - Not Found: Recurso no encontrado
500 - Internal Server Error: Error del servidor

================================================================================
6. SOLUCIÓN DE PROBLEMAS
================================================================================

PROBLEMA 1: Python no se reconoce como comando
--------------------------------------------------------------------------------
Síntoma:
    'python' is not recognized as an internal or external command

Solución:
    # Intenta con python3
    python3 --version
    
    # Windows: Agrega Python al PATH
    1. Busca "Variables de entorno" en el menú de Windows
    2. Edita "Path" en Variables del sistema
    3. Agrega: C:\Python310 (o tu ruta de instalación)
    4. Reinicia la terminal

PROBLEMA 2: Error al crear entorno virtual
--------------------------------------------------------------------------------
Síntoma:
    The virtual environment was not created successfully

Solución Windows:
    python -m pip install virtualenv
    python -m virtualenv venv

Solución Linux/Mac:
    sudo apt-get install python3-venv
    python3 -m venv venv

PROBLEMA 3: Error con PyArrow
--------------------------------------------------------------------------------
Síntoma:
    Failed building wheel for pyarrow
    ERROR: Could not build wheels for pyarrow

Solución:
    # Python 3.12+ tiene problemas con PyArrow
    # Opción 1: Usa Python 3.10 o 3.11 (Recomendado)
    
    # Opción 2: Instala versión específica
    pip uninstall pyarrow -y
    pip install pyarrow==21.0.0 --no-cache-dir

PROBLEMA 4: Archivo CSV no encontrado
--------------------------------------------------------------------------------
Síntoma:
    FileNotFoundError: No such file or directory
    'data/yellow_tripdata_2015-01.csv'

Solución:
    # Verificar que el archivo esté en la ubicación correcta
    # Estructura correcta:
    # Grupo9_MovilidadUrbanaCaso/
    #   ├── data/
    #   │   └── yellow_tripdata_2015-01.csv
    #   └── main.py
    
    # Verificar
    ls data/  # Linux/Mac
    dir data\ # Windows

PROBLEMA 5: Puerto 8000 ya en uso
--------------------------------------------------------------------------------
Síntoma:
    ERROR: [Errno 98] Address already in use
    ERROR: [WinError 10048] Solo se permite un uso de cada dirección

Solución Opción 1 - Usar otro puerto:
    uvicorn api_app:app --host 0.0.0.0 --port 8080 --reload
    
    # Luego actualizar en dashboard.py línea 11:
    API_BASE_URL = "http://localhost:8080"

Solución Opción 2 - Matar el proceso (Windows):
    netstat -ano | findstr :8000
    taskkill /PID [PID_NUMBER] /F

Solución Opción 2 - Matar el proceso (Linux/Mac):
    lsof -ti:8000 | xargs kill -9

PROBLEMA 6: Dashboard no se conecta a la API
--------------------------------------------------------------------------------
Síntoma:
    Error al cargar datos del EDA desde la API
    Connection refused
    [Errno 111] Connection refused

Solución:
    # 1. Verificar que la API esté corriendo
    # Abrir http://localhost:8000/docs en el navegador
    # Si no carga, la API no está corriendo
    
    # 2. Reiniciar la API
    # Terminal 1:
    CTRL+C (detener)
    uvicorn api_app:app --host 0.0.0.0 --port 8000 --reload
    
    # 3. Verificar firewall (Windows)
    # Permitir Python en el Firewall de Windows
    
    # 4. Verificar URL en dashboard.py (línea 11)
    API_BASE_URL = "http://localhost:8000"  # Debe coincidir con puerto API

PROBLEMA 7: Error de memoria al procesar datos
--------------------------------------------------------------------------------
Síntoma:
    MemoryError
    Killed
    El proceso se congela

Solución:
    # 1. Usar un subset del dataset para pruebas
    # Editar data_loader.py, línea 21:
    df = pd.read_csv(path, sep=',', encoding='utf-8', low_memory=False, nrows=100000)
    
    # 2. Cerrar otras aplicaciones para liberar RAM
    
    # 3. Aumentar memoria swap (Linux)
    # 4. Procesar en una máquina con más RAM

PROBLEMA 8: Streamlit no se abre automáticamente
--------------------------------------------------------------------------------
Síntoma:
    El navegador no se abre al ejecutar streamlit run dashboard.py

Solución:
    # Abrir manualmente en el navegador:
    http://localhost:8501
    
    # O configurar Streamlit:
    streamlit run dashboard.py --server.headless=true

PROBLEMA 9: Módulo no encontrado
--------------------------------------------------------------------------------
Síntoma:
    ModuleNotFoundError: No module named 'pandas'
    ModuleNotFoundError: No module named 'fastapi'

Solución:
    # Verificar que el entorno virtual esté activado
    # Debe aparecer (venv) en el prompt
    
    # Reinstalar dependencias
    pip install -r requirements.txt --upgrade
    
    # Verificar instalación
    pip list

PROBLEMA 10: Datos no se muestran en el dashboard
--------------------------------------------------------------------------------
Síntoma:
    Dashboard carga pero muestra:
    "No hay datos para calcular los KPI"
    Mapas vacíos

Solución:
    # 1. Verificar que el archivo procesado existe
    ls data/processed/tripdata_cleaned.csv
    
    # 2. Si no existe, ejecutar pipeline nuevamente
    python main.py
    
    # 3. Verificar logs de la API
    # Buscar errores en Terminal 1 donde corre la API
    
    # 4. Reiniciar ambos servicios
    # CTRL+C en ambas terminales
    # Volver a ejecutar API y Dashboard

COMANDOS ÚTILES PARA DIAGNÓSTICO
--------------------------------------------------------------------------------
# Ver versiones instaladas
pip list

# Ver información de paquete específico
pip show pandas

# Verificar estructura del proyecto
tree  # Windows (si tree está instalado)
ls -R  # Linux/Mac

# Ver procesos Python corriendo
# Windows:
tasklist | findstr python

# Linux/Mac:
ps aux | grep python

# Verificar puertos en uso
# Windows:
netstat -ano | findstr LISTENING

# Linux/Mac:
netstat -tuln | grep LISTEN

# Logs detallados de Streamlit
streamlit run dashboard.py --logger.level=debug

# Logs detallados de API
uvicorn api_app:app --log-level debug

CONTACTO Y SOPORTE
--------------------------------------------------------------------------------
Si encuentras un problema no listado aquí:

1. Revisa los logs de error en las terminales
2. Busca el error específico en la documentación oficial:
   - Python: https://docs.python.org/3/
   - FastAPI: https://fastapi.tiangolo.com/
   - Streamlit: https://docs.streamlit.io/
   - Pandas: https://pandas.pydata.org/docs/

3. Verifica que todos los archivos estén en su ubicación correcta
4. Asegúrate de que el entorno virtual esté activado

CHECKLIST DE VERIFICACIÓN FINAL
--------------------------------------------------------------------------------
Antes de reportar un problema, verifica:

□ Python 3.8-3.11 instalado correctamente
□ Git instalado y repositorio clonado
□ Entorno virtual creado y activado (aparece (venv))
□ Todas las dependencias instaladas sin errores
□ Dataset descargado en data/yellow_tripdata_2015-01.csv
□ Pipeline ejecutado exitosamente (python main.py)
□ Archivo procesado existe en data/processed/tripdata_cleaned.csv
□ API levantada y accesible en http://localhost:8000/docs
□ Dashboard levantado y accesible en http://localhost:8501
□ Sin errores en las consolas de API y Dashboard
□ Visualizaciones cargando correctamente

================================================================================
RESUMEN DE COMANDOS RÁPIDOS
================================================================================

INSTALACIÓN COMPLETA (Primera vez)
--------------------------------------------------------------------------------
git clone https://github.com/tu-usuario/Grupo9_MovilidadUrbanaCaso.git
cd Grupo9_MovilidadUrbanaCaso
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install --upgrade pip
pip install -r requirements.txt
# [Descargar dataset manualmente a data/]
python main.py

EJECUCIÓN DIARIA
--------------------------------------------------------------------------------
# Terminal 1:
cd Grupo9_MovilidadUrbanaCaso
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
uvicorn api_app:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2:
cd Grupo9_MovilidadUrbanaCaso
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
streamlit run dashboard.py

DETENER APLICACIÓN
--------------------------------------------------------------------------------
# En cada terminal:
CTRL+C

# Desactivar entorno:
deactivate

ACTUALIZAR CÓDIGO
--------------------------------------------------------------------------------
git pull origin main
pip install -r requirements.txt --upgrade
python main.py  # Solo si hay cambios en el pipeline

================================================================================
CARACTERÍSTICAS TÉCNICAS DEL SISTEMA
================================================================================

TECNOLOGÍAS UTILIZADAS
--------------------------------------------------------------------------------
Backend:
    • Python 3.10
    • FastAPI 0.121.0 - Framework API REST
    • Uvicorn 0.38.0 - Servidor ASGI
    • Pandas 2.3.3 - Manipulación de datos
    • NumPy 2.3.4 - Operaciones numéricas
    • PyArrow 21.0.0 - Procesamiento eficiente

Frontend:
    • Streamlit 1.51.0 - Framework dashboard
    • PyDeck 0.9.1 - Visualizaciones 3D
    • Plotly 6.3.1 - Gráficos interactivos
    • Requests 2.32.5 - Comunicación HTTP

RENDIMIENTO
--------------------------------------------------------------------------------
Dataset Original:
    • Registros: ~12,906,858 viajes
    • Tamaño: ~1.8 GB
    • Período: Enero 2015

Dataset Procesado:
    • Registros: ~10,906,858 viajes (válidos)
    • Tamaño: ~800 MB
    • Tiempo procesamiento: 5-10 minutos

API:
    • Tiempo respuesta promedio: <500ms
    • Máximo puntos mapa calor: 20,000
    • Máximo flujos por zona: 1,000

Dashboard:
    • Tiempo carga inicial: 2-3 segundos
    • Actualización filtros: 2-5 segundos
    • Renderizado mapas: 3-7 segundos

LIMITACIONES Y CONSIDERACIONES
--------------------------------------------------------------------------------
1. Memoria RAM:
   - Mínimo recomendado: 4GB
   - Óptimo: 8GB o más
   
2. Almacenamiento:
   - Dataset original: 1.8 GB
   - Dataset procesado: 800 MB
   - Entorno virtual: 500 MB
   - Total requerido: ~5 GB

3. Rendimiento Mapas:
   - Los mapas muestran máximo 20,000 puntos
   - Muestreo aleatorio si hay más registros
   - Optimizado para navegadores modernos

4. Navegadores Compatibles:
   - Chrome 90+ (Recomendado)
   - Firefox 88+
   - Edge 90+
   - Safari 14+

5. Red:
   - API y Dashboard corren localmente
   - No requiere conexión a internet después de la instalación
   - Descarga del dataset requiere conexión estable

SEGURIDAD
--------------------------------------------------------------------------------
- API sin autenticación (uso local)
- CORS habilitado para desarrollo
- No almacena datos sensibles de usuarios
- Dataset público de NYC TLC

ESCALABILIDAD
--------------------------------------------------------------------------------
Para producción considerar:
    • Autenticación API (OAuth2, JWT)
    • Base de datos (PostgreSQL + PostGIS)
    • Cache (Redis)
    • Load balancer
    • Despliegue en cloud (AWS, GCP, Azure)

================================================================================
INFORMACIÓN DEL PROYECTO
================================================================================

OBJETIVOS ACADÉMICOS
--------------------------------------------------------------------------------
1. Implementar pipeline de limpieza de datos robusto
2. Filtrar coordenadas fuera del bounding box de NYC
3. Descartar viajes con duración/distancia anómala
4. Crear mapas interactivos de NYC con heatmaps
5. Analizar patrones de movilidad urbana
6. Optimizar rutas y servicios de taxi

ENTREGABLES
--------------------------------------------------------------------------------
✅ Pipeline de procesamiento de datos (main.py + scripts/)
✅ API REST funcional (api_app.py)
✅ Dashboard interactivo (dashboard.py)
✅ Documentación completa (README.md)
✅ Visualizaciones geoespaciales (mapas de calor y flujos)
✅ Análisis de KPIs de movilidad

METODOLOGÍA
--------------------------------------------------------------------------------
1. Análisis exploratorio de datos (EDA)
2. Diseño del pipeline de limpieza
3. Implementación modular (scripts/)
4. Desarrollo de API REST
5. Creación de dashboard interactivo
6. Pruebas y optimización
7. Documentación

APRENDIZAJES CLAVE
--------------------------------------------------------------------------------
- Procesamiento de grandes volúmenes de datos
- Análisis geoespacial con coordenadas
- Desarrollo de APIs REST con FastAPI
- Visualizaciones interactivas con Streamlit y PyDeck
- Ingeniería de características (feature engineering)
- Optimización de rendimiento
- Documentación técnica

================================================================================
LICENCIA Y USO
================================================================================

Este proyecto es de uso académico para el curso de Análisis de Datos 
Geoespaciales.

Dataset: NYC Taxi & Limousine Commission (TLC)
Licencia: Datos públicos

© 2025 Grupo 9 - Análisis de Movilidad Urbana
Todos los derechos reservados para fines académicos.

================================================================================
FIN DEL DOCUMENTO
================================================================================

Para más información, consultar:
- Documentación API: http://localhost:8000/docs
- Dashboard: http://localhost:8501
- Repositorio: https://github.com/tu-usuario/Grupo9_MovilidadUrbanaCaso

Grupo 9:
- Leonardo Mafla
- Vanessa Nasimba
- Edwin Tapia


Última actualización: Noviembre 2025
