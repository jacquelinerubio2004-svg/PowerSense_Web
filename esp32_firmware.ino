#include <WiFi.h>
#include <HTTPClient.h>
#include "EmonLib.h"

EnergyMonitor SCT013;

// CONFIGURA: rellena con tu WiFi y la URL pública de ngrok (http://xxxx.ngrok.io)
const char* ssid = "TU_SSID";
const char* pass = "TU_PASS";
const char* serverUrl = "http://REEMPLAZA_CON_NGROK_URL/api/consumo"; // usa http o https según ngrok
const char* api_key = "AQUI_TU_API_KEY";

int pinSCT = 36;       // ADC pin
int tension = 230;     // Voltaje de la red (ajusta a 120 si corresponde)
float calibration = 0.0607; // valor inicial de calibración (ajusta)

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, pass);

  SCT013.current(pinSCT, calibration);

  Serial.print("Conectando a WiFi");
  unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if (millis() - start > 20000) break; // no bloquear indefinidamente
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
    http.begin(serverUrl); // soporta http:// y https:// en la mayoría de builds
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

  delay(5000); // ajusta según necesidad
}
