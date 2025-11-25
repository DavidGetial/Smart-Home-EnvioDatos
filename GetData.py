# GetData.py → Envía a Supabase + ThingSpeak (FUNCIONA PERFECTO 2025)
import serial
import time
import urllib.parse
import http.client
from getPort import port
from supabase import create_client, Client

# ==================== SUPABASE ====================
url = "https://uyfqzfogryrhvofqkivu.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV5ZnF6Zm9ncnlyaHZvZnFraXZ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3MzI2NTQsImV4cCI6MjA3NzMwODY1NH0.MxGmnnrse-8hCfv1qtO8g7ZlmDNJh-Amt8_ak_1htEI"
supabase: Client = create_client(url, key)

# ==================== THINGSPEAK ====================
THINGSPEAK_API_KEY = "2MBL2ZJD5LFCBT44"

# ==================== ARDUINO ====================
arduino_port = port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)

print(f"Board detected on port: {arduino_port}")
print("Conectado → Enviando a Supabase y ThingSpeak cada 15 segundos...\n")

try:
    while True:
        data = ser.readline().decode('utf-8').rstrip()
        if data:
            try:
                humidity, temperature = data.split(",")
                humidity = float(humidity)
                temperature = float(temperature)

                # --- ENVÍO A SUPABASE ---
                supabase.table("data").insert({
                    "humidity": humidity,
                    "temperature": temperature
                }).execute()
                print(f"Supabase → {temperature}°C | {humidity}%")

                # --- ENVÍO A THINGSPEAK ---
                try:
                    params = urllib.parse.urlencode({
                        'api_key': THINGSPEAK_API_KEY,
                        'field1': temperature,
                        'field2': humidity
                    })
                    headers = {"Content-type": "application/x-www-form-urlencoded"}
                    conn = http.client.HTTPSConnection("api.thingspeak.com")
                    conn.request("POST", "/update", params, headers)
                    response = conn.getresponse()
                    result = response.read().decode()

                    if response.status == 200 and result != "0":
                        print(f"ThingSpeak → {temperature}°C | {humidity}% (OK)\n")
                    else:
                        print(f"ThingSpeak error → código: {response.status} | respuesta: {result}\n")
                    conn.close()

                except Exception as e:
                    print(f"Error ThingSpeak → {e}\n")

            except ValueError:
                print(f"Formato inválido → {data}")
            except Exception as e:
                print(f"Error Supabase → {e}")

        time.sleep(15)

except KeyboardInterrupt:
    print("\nDetenido por el usuario. Cerrando puerto...")
finally:
    ser.close()
    print("Puerto cerrado. ¡Todo bien!")