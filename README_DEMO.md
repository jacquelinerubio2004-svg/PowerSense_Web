PowerSense — Demo (instrucciones rápidas)

Objetivo
- Versión simplificada para presentación: servidor Flask + SQLAlchemy (SQLite por defecto) y firmware demo para ESP32.

Archivos importantes
- `app.py` — servidor Flask (login/register/dashboard/devices/api)
- `db_sql.py` — acceso SQL con SQLAlchemy (usa `DATABASE_URL`, por defecto SQLite)
- `esp32_firmware_demo.ino` — firmware plantilla para la ESP32 (reemplaza `SSID`, `PASSWORD`, `SERVER_URL`, `API_KEY` antes de compilar)
- `presentation.md` — guion y diapositivas para la demo

Cómo usar la demo localmente (rápido)
1. Clona el repo y entra en la carpeta:
   ```powershell
   git clone https://github.com/jacquelinerubio2004-svg/PowerSense_Web
   cd PowerSense_Web
   ```
2. Crea entorno y dependencias:
   ```powershell
   python -m venv .venv
   . .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Ejecuta la app (SQLite por defecto):
   ```powershell
   $env:HOST = "127.0.0.1"
   python app.py
   ```
4. En el navegador: `http://127.0.0.1:5000` → `/register` → crear cuenta profesor → `/devices` → crear dispositivo → copia `api_key`.
5. Edita `esp32_firmware_demo.ino` y reemplaza:
   - `TU_SSID`, `TU_PASS`
   - `REEMPLAZA_CON_URL_DEL_SERVIDOR` por `http://<IP_DEL_PC>:5000` si pruebas local
   - `REEMPLAZA_CON_API_KEY` por la clave copiada
6. Compila y sube la ESP32 desde Arduino IDE o PlatformIO.

Nota sobre GitHub
- La rama `demo` contiene todo lo necesario para la presentación. Si quieres que el repositorio `main` también refleje exactamente esta versión, puedo reemplazar `main` por `demo` (esto sobreescribirá la historia de `main`). Si estás de acuerdo, dime y hago el cambio.
