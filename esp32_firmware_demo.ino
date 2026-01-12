/*
  PowerSense - Firmware demo (ESP32)
  - Antes de compilar: reemplaza los placeholders con tu información
    - SSID y PASSWORD de tu WiFi
    - SERVER_URL: la URL pública o la IP local de tu servidor + /api/consumo
    - API_KEY: la clave generada desde la web en /devices

  Ejemplo:
    const char* serverUrl = "https://mi-app.onrender.com/api/consumo";
    const char* api_key = "11111111-2222-3333-4444-555555555555";
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include "EmonLib.h"

EnergyMonitor SCT013;

// CONFIGURA: rellena con tu WiFi y la URL del servidor
const char* ssid = "TU_SSID";          // <- reemplaza
const char* pass = "TU_PASS";          // <- reemplaza
const char* serverUrl = "REEMPLAZA_CON_URL_DEL_SERVIDOR/api/consumo"; // <- reemplaza
const char* api_key = "REEMPLAZA_CON_API_KEY"; // <- reemplaza

int pinSCT = 36;       // ADC pin (ajusta si usas otro)
int tension = 230;     // Voltaje de la red (cambia a 120 si aplica)
float calibration = 0.0607; // valor de calibración inicial

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, pass);

  SCT013.current(pinSCT, calibration);

  Serial.print("Conectando a WiFi");
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if (millis() - start > 20000) break; // timeout
  }
  Serial.println();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi conectado");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("No se conectó a WiFi");
  }
}

void loop() {
  double Irms = SCT013.calcIrms(4096); // RMS en Amperios
  double potencia = Irms * tension;    // Potencia en W

  Serial.print("Irms: "); Serial.print(Irms, 3);
  Serial.print(" A, Potencia: "); Serial.print(potencia, 2); Serial.println(" W");

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String payload = "{";
    payload += "\"api_key\":\"" + String(api_key) + "\",";
    payload += "\"valor\":" + String(potencia, 2);
    payload += "}";

    int code = http.POST(payload);
    if (code > 0) {
      Serial.print("HTTP POST code: "); Serial.println(code);
      String resp = http.getString();
      Serial.println(resp);
    } else {
      Serial.print("Error POST: "); Serial.println(code);
    }
    http.end();
  } else {
    Serial.println("WiFi no conectado - reintentando conexión...");
    WiFi.reconnect();
  }

  delay(5000); // enviar cada 5s
}
