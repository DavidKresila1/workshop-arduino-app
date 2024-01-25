import random
from datetime import datetime, timezone, timedelta

# Function to generate random temperature data
def generate_temperature():
    return round(random.uniform(20.0, 30.0), 2)

# Function to generate a timestamp in UTC
def generate_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

# Generate and log sample data
for _ in range(10):  # Generate data for 10 iterations
    simulated_temperature = generate_temperature()
    timestamp = generate_timestamp()

    with open("data.txt", "a") as file:
        file.write(f"{timestamp}: Temperature {simulated_temperature}\n")
