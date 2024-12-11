from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
import socket
import os

# MongoDB Configuration
MONGO_URI = "mongodb+srv://lenardjirehabelita01:Pt2Tqz354cyhO8Ow@cluster0.kjj3i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB_NAME = "Cluster0"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Query 1: Average moisture in the fridge
def calculate_query_1():
    virtual = db["sensor_data"]  # Replace with your collection name
    metadata = db["device_metadata"]  # Replace with your collection name

    three_hours_ago = datetime.now(tz=timezone.utc) - timedelta(hours=3)
    three_hours_ago_unix = int(three_hours_ago.timestamp())

    device = metadata.find_one({
        "eventTypes": {"$in": ["Moisture Monitoring"]},
        "customAttributes.additionalMetadata.Location": "Kitchen"
    })
    if not device:
        return "No matching device found for query 1."

    device_id = device["assetUid"]

    results = virtual.find({
        "payload.parent_asset_uid": device_id,
        "$expr": {"$gte": [{"$toLong": "$payload.timestamp"}, three_hours_ago_unix]},
        "payload.Moisture Meter - Fridge": {"$exists": True}
    })
    humidities = [float(result["payload"]["Moisture Meter - Fridge"]) for result in results]

    if not humidities:
        return "No readings available in the last 3 hours."

    average_humidity = sum(humidities) / len(humidities)
    return f"Average relative humidity in the fridge: {average_humidity:.2f}% RH"

# Query 2: Average water consumption
def calculate_query_2():
    virtual = db["sensor_data"]
    metadata = db["device_metadata"]

    device = metadata.find_one({
        "eventTypes": {"$in": ["Water Consumption Monitoring"]}
    })
    if not device:
        return "No matching device found for query 2."

    device_id = device["assetUid"]

    results = virtual.find({
        "payload.parent_asset_uid": device_id,
        "payload.Water_consumption_sensor_DW": {"$exists": True}
    })
    consumptions = [float(doc["payload"]["Water_consumption_sensor_DW"]) for doc in results]

    if not consumptions:
        return "No water consumption data available."

    average_consumption = sum(consumptions) / len(consumptions)
    return f"Average water consumption per cycle: {average_consumption:.2f} gallons"

# Query 3: Device with highest electricity consumption
def calculate_query_3():
    virtual = db["sensor_data"]
    metadata = db["device_metadata"]

    devices = metadata.find({
        "eventTypes": {"$in": ["Electricity Consumption"]}
    })

    consumption_data = {}
    for device in devices:
        device_id = device["assetUid"]
        device_name = device["customAttributes"].get("name", f"Device {device_id}")

        results = virtual.find({
            "payload.parent_asset_uid": device_id,
            "payload.Electricity_Consumption": {"$exists": True}
        })

        total_consumption = sum(float(doc["payload"]["Electricity_Consumption"]) for doc in results)
        consumption_data[device_name] = total_consumption

    if not consumption_data:
        return "No electricity consumption data available."

    max_device = max(consumption_data, key=consumption_data.get)
    return f"{max_device} consumed the most electricity with {consumption_data[max_device]:.2f} kWh"

# TCP Server
def tcp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((host, port))
    except Exception as e:
        print(f"Error binding server: {e}")
        return

    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client connected: {client_address}")

        query = int(client_socket.recv(1024).decode())
        if query == 1:
            response = calculate_query_1()
        elif query == 2:
            response = calculate_query_2()
        elif query == 3:
            response = calculate_query_3()
        else:
            response = "Invalid query. Use 1, 2, or 3."

        client_socket.send(response.encode())
        client_socket.close()

# Main
if __name__ == "__main__":
    host = "localhost"
    port = 9090
    tcp_server(host, port)
