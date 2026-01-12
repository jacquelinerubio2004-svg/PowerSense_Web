#!/usr/bin/env python3
"""
Simulador de ESP32 para PowerSense Demo
- Envía datos de consumo al servidor para pruebas sin hardware real
- Usa requests para POST a /api/consumo
"""

import requests
import time
import random

# CONFIGURA ESTOS VALORES
SERVER_URL = "http://127.0.0.1:5000/api/consumo"  # cambia a la URL de tu servidor
API_KEY = "AQUI_REEMPLAZA_CON_TU_API_KEY"  # copia del paso 6 (dispositivos)

def enviar_consumo(valor):
    """Envía un valor de consumo al servidor."""
    payload = {
        "api_key": API_KEY,
        "valor": valor
    }
    try:
        response = requests.post(SERVER_URL, json=payload)
        if response.status_code == 200:
            print(f"✓ Consumo enviado: {valor} W - Respuesta: {response.json()}")
        else:
            print(f"✗ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"✗ Error de conexión: {e}")

def main():
    print("=" * 60)
    print("Simulador de ESP32 — PowerSense")
    print("=" * 60)
    print(f"Servidor: {SERVER_URL}")
    print(f"API Key: {API_KEY}")
    print()
    
    # Genera 5 lecturas con valores aleatorios (30-100 W)
    for i in range(1, 6):
        consumo = random.uniform(30, 100)
        print(f"[{i}/5] Enviando lectura: {consumo:.2f} W...")
        enviar_consumo(round(consumo, 2))
        time.sleep(2)  # espera 2s entre lecturas
    
    print()
    print("✓ Demo completada. Verifica el dashboard en el navegador.")
    print("=" * 60)

if __name__ == "__main__":
    main()
