
import serial
import requests
import time

# 1. Connect to Arduino UNO
arduino = serial.Serial('COM7', 9600, timeout=2)
time.sleep(2)

# 2. Enter your ThingSpeak WRITE API KEY
API_KEY = "39SXLJAL7ZESVZVR"

# 3. ThingSpeak upload address
url = "https://api.thingspeak.com/update"

print("Arduino connected!")
print("Uploading temperature to ThingSpeak...")

last_upload = 0

while True:
    line = arduino.readline().decode(
        "utf-8", errors="ignore"
    ).strip()

    if line.startswith("Temperature:"):
        try:
            temperature = float(
                line.replace("Temperature:", "")
                    .replace("C", "")
                    .replace("°", "")
                    .strip()
            )

            print("Temperature:", temperature, "C")

            if time.time() - last_upload >= 20:
                response = requests.get(
                    url,
                    params={
                        "api_key": API_KEY,
                        "field1": temperature
                    },
                    timeout=10
                )

                print("ThingSpeak response:", response.text)
                last_upload = time.time()

        except ValueError:
            print("Could not read temperature:", line)
        except requests.RequestException as error:
            print("Cloud upload error:", error)
