import serial.tools.list_ports

def detectBoardPort():
    ports = serial.tools.list_ports.comports()

    for port in ports:
        if "ESP32" in port.description or "CH34" in port.description:
            """print(f"Board description: {port.description}")
            print(f"Board device: {port.device}")
            print(f"Board name: {port.name}")
            print(f"HWID: {port.hwid}")
            print(f"Vendor ID: {port.vid}")
            print(f"Manufacturer: {port.manufacturer}")
            print(f"Location: {port.location}")"""
            return port.device
    return None

port = detectBoardPort()

if port:
    print(f"Board detected on port: {port}")
else:
    print("No board port detected")