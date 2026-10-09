from pymodbus.client import ModbusTcpClient
import time

def run_hmi_client():
    client = ModbusTcpClient("127.0.0.1", port=5020)
    connection = client.connect()
    
    if not connection:
        print("Failed to connect to the PLC Server!")
        return
        
    print("HMI Client successfully connected to Virtual PLC. Reading holding registers...")
    
    try:
        while True:
            result = client.read_holding_registers(address=0, count=5)
            if not result.isError():
                print(f"Holding Registers [0-4]: {result.registers}")
            else:
                print("Error reading from PLC registers.")
            time.sleep(2)
    except KeyboardInterrupt:
        client.close()
        print("HMI Client disconnected and stopped safely.")

if __name__ == "__main__":
    run_hmi_client()