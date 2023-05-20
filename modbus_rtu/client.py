from modbus_frames import response_frames
from modbus_frames import functions_codes as fc
import serial

def crc(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for i in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, byteorder="big")

class ModbusRtuClient():
    def __init__(self,server_address, port, baudrate, timeout):
        self._server_address = server_address
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._serial = serial.Serial(port, baudrate, timeout=timeout)            


        
    def read_coils(self, server_address,start_address, quantity):
        self._server_address = server_address
        request = request_frames.read_coils(start_address,quantity)
        request = server_address.to_bytes(2,byteorder="big") + request + crc(request)
        self._serial.write(request)
        response = self._serial.read(5 + quantity // 8 + (1 if quantity % 8 else 0))
        if response[0] != server_address:
            raise Exception("Wrong server address")
        if response[1] != fc.read_coils:
            raise Exception("Wrong function code")
        if response[2] != quantity // 8 + (1 if quantity % 8 else 0):
            raise Exception("Wrong byte count")
        if crc(response[:-2]) != response[-2:]:
            raise Exception("Wrong CRC")
        return response[3:-2]
    
    def read_discrete_inputs(self, server_address,start_address, quantity):
        self._server_address = server_address
        request = request_frames.read_discrete_inputs(start_address,quantity)
        request = server_address.to_bytes(2,byteorder="big") + request + crc(request)
        self._serial.write(request)
        response = self._serial.read(5 + quantity // 8 + (1 if quantity % 8 else 0))
        if response[0] != server_address:
            raise Exception("Wrong server address")
        if response[1] != fc.read_discrete_inputs:
            raise Exception("Wrong function code")
        if response[2] != quantity // 8 + (1 if quantity % 8 else 0):
            raise Exception("Wrong byte count")
        if crc(response[:-2]) != response[-2:]:
            raise Exception("Wrong CRC")
        return response[3:-2]
    
    def read_holding_registers(self, server_address,start_address, quantity):
        self._server_address = server_address
        request = request_frames.read_holding_registers(start_address,quantity)
        request = server_address.to_bytes(2,byteorder="big") + request + crc(request)
        self._serial.write(request)
        response = self._serial.read(5 + quantity * 2)
        if response[0] != server_address:
            raise Exception("Wrong server address")
        if response[1] != fc.read_holding_registers:
            raise Exception("Wrong function code")
        if response[2] != quantity * 2:
            raise Exception("Wrong byte count")
        if crc(response[:-2]) != response[-2:]:
            raise Exception("Wrong CRC")
        return response[3:-2]

    def read_input_registers(self, server_address,start_address, quantity):
        self._server_address = server_address
        request = request_frames.read_input_registers(start_address,quantity)
        request = server_address.to_bytes(2,byteorder="big") + request + crc(request)
        self._serial.write(request)
        response = self._serial.read(5 + quantity * 2)
        if response[0] != server_address:
            raise Exception("Wrong server address")
        if response[1] != fc.read_input_registers:
            raise Exception("Wrong function code")
        if response[2] != quantity * 2:
            raise Exception("Wrong byte count")
        if crc(response[:-2]) != response[-2:]:
            raise Exception("Wrong CRC")
        return response[3:-2]

    def write_single_coil(self, server_address,address, value):
        self._server_address = server_address
        request = request_frames.write_single_coil(address,value)
        request = server_address.to_bytes(2,byteorder="big") + request + crc(request)
        self._serial.write(request)
        response = self._serial.read(8)
        if response[0] != server_address:
            raise Exception("Wrong server address")
        if response[1] != fc.write_single_coil:
            raise Exception("Wrong function code")
        if crc(response[:-2]) != response[-2:]:
            raise Exception("Wrong CRC")
        return response[3:-2]
    
    def write_single_register(self, server_address,address, value):
        self._server_address = server_address
        request = request_frames.write_single_register(address,value)
        request = server_address.to_bytes(2,byteorder="big") + request + crc(request)
        self._serial.write(request)
        response = self._serial.read(8)
        if response[0] != server_address:
            raise Exception("Wrong server address")
        if response[1] != fc.write_single_register:
            raise Exception("Wrong function code")
        if crc(response[:-2]) != response[-2:]:
            raise Exception("Wrong CRC")
        return response[3:-2]
    
    def write_multiple_coils(self, server_address,start_address, values):
        self._server_address = server_address
        request = request_frames.write_multiple_coils(start_address,values)
        request = server_address.to_bytes(2,byteorder="big") + request + crc(request)
        self._serial.write(request)
        response = self._serial.read(8)
        if response[0] != server_address:
            raise Exception("Wrong server address")
        if response[1] != fc.write_multiple_coils:
            raise Exception("Wrong function code")
        if crc(response[:-2]) != response[-2:]:
            raise Exception("Wrong CRC")
        return response[3:-2]

    
