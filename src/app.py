from flask import Flask, jsonify
from serial import Serial, SerialException
import time
from datetime import datetime, timezone
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

ARDUINO_PORT = "/dev/ttyUSB0"  # Update for actual port

try:
    arduino = Serial(port=ARDUINO_PORT, baudrate=9600, timeout=.1)
except SerialException as error:
    print(f"[+] Error while opening serial connection: {error}")
    exit(1)

def read_temperature():
    retries = 25
    for _ in range(retries):
        try:
            arduino.read(arduino.in_waiting)
            time.sleep(0.05)
            arduino.readline()
            raw_data = arduino.readline().decode("utf-8").strip()

            print(f"Raw Data: {raw_data}")

            if not raw_data:
                print("[+] Empty data trying again...")
                continue  # Retry if data is empty

            temperature_parts = [part for part in raw_data.split() if part.replace('.', '').isdigit()]

            if not temperature_parts:
                print(f"Invalid data received: {raw_data}, Retrying...")
                continue  # Retry if temperature data is invalid

            temperature_value = float(f"{temperature_parts[-1]}")

            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

            with open("data.txt", "a") as file:
                file.write(f"{timestamp}: Temperature {temperature_value}\n")

            return round(temperature_value, 1)
        except SerialException as error:
            print(f"Serial communication error: {error}, Retrying...")
        except ValueError as error:
            print(f"Error converting data to float: {error}, Raw data: {raw_data}")

    print("Failed after multiple retries.")
    return None


def read_data_from_file():
    try:
        with open("data.txt", "r") as file:
            lines = file.readlines()

            if lines:
                latest_entry = lines[-1]
                print("Latest Entry:")
                print(latest_entry)

                temperature_part = latest_entry.split(":")[-1].strip()

                # Extracting the temperature value after the word 'Temperature'
                latest_temperature = float(temperature_part.split()[1])
                latest_temperature = round(latest_temperature, 1)

                return latest_temperature
            else:
                print("No temperature data found in the file.")
                return None

    except Exception as error:
        print(f"Error reading temperature from file: {error}")
        return None


@app.route('/temperature', methods=['GET'])
def get_temperature():
    # Call the function to read data from the file
    latest_temperature = read_temperature()

    # Check if data retrieval was successful
    if latest_temperature is not None:
        # Return the temperature as JSON
        return jsonify({'temperature': latest_temperature})

    else:
        # Return an error message if data retrieval failed
        return jsonify({'error': 'Failed to get data'}), 500


if __name__ == "__main__":
    app.run(port=3040)
