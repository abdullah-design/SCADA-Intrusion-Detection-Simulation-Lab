from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusSlaveContext
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

def run_plc_server():
    print("Starting Virtual PLC (Modbus TCP Server) on localhost:5020...")
    
    store = ModbusServerContext(
        slaves=ModbusSlaveContext(
            di=ModbusSequentialDataBlock(0, [17]*100),
            co=ModbusSequentialDataBlock(0, [0]*100),
            hr=ModbusSequentialDataBlock(0, [100]*100),
            ir=ModbusSequentialDataBlock(0, [50]*100)
        ),
        single=True
    )

    StartTcpServer(context=store, address=("127.0.0.1", 5020))

if __name__ == "__main__":
    run_plc_server()