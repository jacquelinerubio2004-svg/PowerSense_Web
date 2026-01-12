# PowerSense Demo — Para usar en clase

## ¿Qué es esto?

Una aplicación web simple para demostrar cómo medir consumo eléctrico con una **ESP32** y un sensor **SCT013**, enviando los datos a un servidor Flask que los almacena en una base de datos SQL.

## Requisitos previos

- **Python 3.8+** instalado.
- **Git** instalado.
- Opcionalmente: **Arduino IDE** o **PlatformIO** (si usas ESP32 real).
- Una **ESP32** con circuito SCT013 (opcional — puedes probar con el simulador).

## Instalación rápida (5 minutos)

### 1. Clona el repositorio

```powershell
cd C:\Users\Aaron\OneDrive\Desktop
git clone -b demo https://github.com/jacquelinerubio2004-svg/PowerSense_Web PowerSense_Demo
cd PowerSense_Demo
```

### 2. Crea el entorno Python

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Ejecuta el servidor

```powershell
$env:HOST = "127.0.0.1"
python app.py
```

Verás en la consola:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

## Demo en clase (paso a paso)

### Navegador — Crear usuario profesor

1. Abre `http://127.0.0.1:5000` en el navegador.
2. Haz clic en **"Crear cuenta"**.
3. Rellena:
   - **Nombre:** Profesor Demo
   - **Correo:** profesor@demo.com
   - **Contraseña:** 1234
4. Haz clic en **"Registrar"**.
5. Inicia sesión con esas credenciales.

### Navegador — Crear dispositivo y obtener API Key

1. Desde el dashboard, haz clic en **"Dispositivos"**.
2. Rellena: **Nombre del dispositivo:** `Mi Sensor ESP32`.
3. Haz clic en **"Crear dispositivo"**.
4. **Copia el `api_key`** de la tabla (es un UUID largo).

### Opción A — Prueba sin ESP32 (simulador Python)

#### Terminal 2 — Ejecuta el simulador

```powershell
# Asegúrate de estar en la carpeta PowerSense_Demo
. .venv\Scripts\Activate.ps1

# Edita simulate_esp32.py con tu editor favorito
# Busca: API_KEY = "AQUI_REEMPLAZA_CON_TU_API_KEY"
# Reemplazala con la API Key copiada en el paso anterior

python simulate_esp32.py
```

Verás:
```
[1/5] Enviando lectura: 45.32 W...
✓ Consumo enviado: 45.32 W - Respuesta: {'ok': True}
...
```

#### Navegador — Verifica el dashboard

Refresca `http://127.0.0.1:5000/dashboard` (F5). Verás:
- **"Consumo actual: XX.XX W"** (última lectura)
- **"Historial de consumo"** con todas las lecturas

### Opción B — Prueba CON ESP32 real

#### Edita el firmware

Abre `esp32_firmware_demo.ino` en Arduino IDE o PlatformIO y reemplaza:

```cpp
const char* ssid = "TU_SSID";                              // tu WiFi
const char* pass = "TU_PASS";                              // contraseña WiFi
const char* serverUrl = "REEMPLAZA_CON_URL_DEL_SERVIDOR"; // URL del servidor
const char* api_key = "REEMPLAZA_CON_API_KEY";             // API Key del paso anterior
```

**Ejemplo:**
```cpp
const char* ssid = "Mi_Red_WiFi";
const char* pass = "Contraseña123";
const char* serverUrl = "http://192.168.1.100:5000/api/consumo";  // IP de tu PC en la LAN
const char* api_key = "f1a2b3c4-d5e6-f7g8-h9i0-j1k2l3m4n5o6";
```

Para obtener la IP de tu PC:
```powershell
ipconfig
# Busca "IPv4 Address" en tu adaptador WiFi
```

#### Compila y sube a la ESP32

1. Abre Arduino IDE o PlatformIO.
2. Abre `esp32_firmware_demo.ino`.
3. Selecciona la placa ESP32 y el puerto.
4. Compila y sube.

#### Monitorea en Serial Monitor

Arduino IDE → Tools → Serial Monitor (baud rate 115200)

Deberías ver:
```
Conectando a WiFi...
WiFi conectado
Irms: 0.123 A, Potencia: 28.29 W
HTTP POST code: 200
...
```

#### Verifica en el navegador

Refresca el dashboard y verás las lecturas llegando cada 5 segundos.

## Estructura de archivos

```
PowerSense_Demo/
├── app.py                      # Servidor Flask
├── db_sql.py                   # Modelos SQLAlchemy (usuarios, dispositivos, consumo)
├── requirements.txt            # Dependencias Python
├── Procfile                    # Para despliegue (Heroku/Render)
├── presentation.md             # Diapositivas y guion para presentar
├── README_DEMO.md              # Instrucciones (este archivo)
├── esp32_firmware_demo.ino     # Código para la ESP32
├── simulate_esp32.py           # Simulador sin hardware
├── templates/                  # Plantillas HTML
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── devices.html
└── static/                     # Archivos estáticos
    └── style.css
```

## Solución de problemas

| Problema | Solución |
|----------|----------|
| "Module not found: db_sql" | Asegúrate de estar en `PowerSense_Demo/` y de haber ejecutado `pip install -r requirements.txt`. |
| "Port 5000 already in use" | Cierra otra instancia de Flask o usa un puerto diferente: `$env:FLASK_PORT = "5001"` y edita `app.py`. |
| "API Key inválido" en simulator | Copia exactamente el UUID de la tabla de dispositivos, sin espacios. |
| ESP32 no se conecta a WiFi | Verifica SSID, contraseña y que estén en el mismo rango de red. |
| "Connection refused" al enviar datos | Asegúrate de que el servidor sigue corriendo en Terminal 1 (`python app.py`). |

## Próximas mejoras (después de la clase)

- Desplegar en Render (Postgres gestionado + HTTPS).
- Añadir gráficas en tiempo real (Chart.js).
- Implementar autenticación más fuerte (tokens JWT).
- Rate limiting en el endpoint `/api/consumo`.

## Contacto

Si tienes dudas, revisa:
- `presentation.md` (guion para la clase)
- `README_DEMO.md` (este archivo)

¡Buena suerte con la presentación! 🚀
