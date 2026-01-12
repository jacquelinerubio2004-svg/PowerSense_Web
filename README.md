# PowerSense — despliegue y seguridad

Resumen rápido
- Esta app usa Flask + SQLite y tiene endpoints web y `/api/consumo` para recibir datos desde una ESP32.

Archivos clave
- `app.py` — aplicación Flask.
- `database.py` — funciones de acceso a SQLite (ahora usa hash de contraseñas y `DATABASE_PATH`).
- `devices.html`, `dashboard.html`, `login.html`, `register.html` — plantillas.

Dependencias
Instala dependencias en un virtualenv:

```bash
python -m venv .venv
. .venv/bin/activate   # Linux/macOS
. .venv/Scripts/Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

Ejecución local
- Para desarrollo (acceso local):

```powershell
$env:FLASK_DEBUG = "True"
python app.py
```

- Para permitir acceso desde la red local (ESP32 y PC en la misma Wi‑Fi):
  - Edita `HOST` o exporta `HOST=0.0.0.0` y ejecuta:

```powershell
$env:HOST = "0.0.0.0"
python app.py
```
  - Averigua la IP LAN de tu PC con `ipconfig` y usa `http://<IP>:5000` en la ESP32.
  - Asegura el puerto 5000 en el firewall de Windows.

Despliegue en la nube (opciones rápidas)
1) Deploy a Render / Railway / Heroku (recomendado para comenzar)
- Subir repo a GitHub.
- Crear servicio web en Render/Heroku y vincular el repo.
- Variables de entorno recomendadas:
  - `SECRET_KEY` — cadena aleatoria
  - `DATABASE_PATH` — para SQLite (si usas SQLite) o conexión a DB gestionada
  - `FLASK_DEBUG=false`
- Render/Heroku ejecutará `web: gunicorn app:app` desde `Procfile`.

2) Despliegue en VPS y configurar Nginx + Gunicorn + Certbot (Let's Encrypt)
- Instala Python, crea virtualenv, instala `requirements.txt`.
- Ejecuta `gunicorn --bind 127.0.0.1:8000 app:app`.
- Configura Nginx como reverse proxy a `127.0.0.1:8000` y obtén certificados TLS con Certbot.

Uso de HTTPS sin administrar el servidor: Cloudflare Tunnel / Cloud Run / Fly.io
- Fly.io o Cloud Run te dan URLs seguras sin manejar Certbot.

Seguridad mínima aplicada en el repo
- `database.py` ahora guarda contraseñas con hashing (`werkzeug.security`).
- `app.py` lee `SECRET_KEY` desde `SECRET_KEY` env var.

Siguientes pasos recomendados
- Cambiar SQLite por una DB gestionada (Postgres) para producción.
- Añadir autenticación API para usuarios/admin (tokens JWT si necesitas más control).
- Implementar rate-limiting en `/api/consumo`.
- Habilitar HTTPS (usando Render/Heroku/Fly or Nginx+Certbot).

Si quieres, te guío en uno de estos flujos:
- Opción A: desplegar en Render (rápido) y configurar HTTPS automático.
- Opción B: usar `ngrok` para exponer temporalmente con HTTPS.
- Opción C: configurar VPS + Nginx + Let's Encrypt (más avanzado).

Indica cuál prefieres y lo hago paso a paso.

---

Ngrok — guía rápida para pruebas remotas
1. Regístrate y descarga `ngrok` desde https://ngrok.com/download.
2. Autentica tu cliente (solo la primera vez) con tu `authtoken`:

```powershell
ngrok config add-authtoken <TU_AUTHTOKEN>
```

3. Arranca tu servidor Flask localmente (desde la carpeta del proyecto):

```powershell
$env:HOST = "0.0.0.0"
python app.py
```

4. En otra terminal lanza ngrok para exponer el puerto 5000:

```powershell
ngrok http 5000
```

5. Ngrok mostrará una URL pública, p.ej. `https://abcd1234.ngrok.io` y `http://abcd1234.ngrok.io`.
  - Copia la URL HTTP o HTTPS y pégala en la variable `serverUrl` dentro de `esp32_firmware.ino`, por ejemplo:

```
const char* serverUrl = "http://abcd1234.ngrok.io/api/consumo";
```

6. Sube el firmware a la ESP32 (con `api_key` correcto) y valida que lleguen peticiones al servidor.

Pruebas rápidas desde tu PC (antes de la ESP32):

```powershell
# prueba POST con PowerShell
Invoke-RestMethod -Method Post -Uri https://abcd1234.ngrok.io/api/consumo -Body '{"api_key":"LA_API_KEY","valor":42.5}' -ContentType 'application/json'
```

Notas:
- Para producción no uses ngrok permanentemente; es para pruebas y demos.
- Si la ESP32 necesita HTTPS, usa la URL `https://...` y asegúrate de que tu build soporte TLS (algunas placas/SDK requieren configurar `WiFiClientSecure`).
- Cuando quieras pasar a producción, desplegamos en Render/Fly/Heroku y configuramos base de datos gestionada y HTTPS permanente.
