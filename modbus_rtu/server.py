from modbus_frames import response_frames
from modbus_frames import functions_codes as fc
import serial
class ModbusRtuServer():
    def __init__(self, port, baudrate, timeout, coils, discrete_inputs, holding_registers, input_registers):
        self._server_address = server_address
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._coils = coils 
        self._discrete_inputs = discrete_inputs
        self._holding_registers = holding_registers
        self._input_registers = input_registers
        self._serial = serial.Serial(port, baudrate, timeout=timeout)

    def  check_for_requests(self):
        # Read from serial port
        # Check if request is for this server
        # If so, parse request and build response
        # Write response to serial port
        try:
            if(self._serial.read(2) == self._server_address.to_bytes(2,byte_order="big")):
                function_code = self.serial.read(1)

                if(function_code == fc.read_coils):
                    start_address = int.from_bytes(self._serial.read(2), byteorder="big")
                    quantity = int.from_bytes(self._serial.read(2), byteorder="big")
                    response = response_frames.read_coils(start_address,quantity)
                    self._serial.write(response)

                elif(function_code == fc.read_discrete_inputs):
                    start_address = int.from_bytes(self._serial.read(2), byteorder="big")
                    quantity = int.from_bytes(self._serial.read(2), byteorder="big")
                    response = response_frames.read_discrete_inputs(start_address,quantity)
                    self._serial.write(response)

                elif(function_code == fc.read_holding_registers):
                    start_address = int.from_bytes(self._serial.read(2), byteorder="big")
                    quantity = int.from_bytes(self._serial.read(2), byteorder="big")
                    response = response_frames.read_holding_registers(start_address,quantity)
                    self._serial.write(response)

                elif(function_code == fc.read_input_registers):
                    start_address = int.from_bytes(self._serial.read(2), byteorder="big")
                    quantity = int.from_bytes(self._serial.read(2), byteorder="big")
                    response = response_frames.read_input_registers(start_address,quantity)
                    self._serial.write(response)

                elif(function_code == fc.write_single_coil):
                    address = int.from_bytes(self._serial.read(2), byteorder="big")
                    value = int.from_bytes(self._serial.read(2), byteorder="big")
                    response = response_frames.write_single_coil(address,value)
                    self._serial.write(response)

                elif(function_code == fc.write_single_register):
                    address = int.from_bytes(self._serial.read(2), byteorder="big")
                    value = int.from_bytes(self._serial.read(2), byteorder="big")
                    response = response_frames.write_single_register(address,value)
                    self._serial.write(response)

                elif(function_code == fc.write_multiple_coils):
                    start_address = int.from_bytes(self._serial.read(2), byteorder="big")
                    quantity = int.from_bytes(self._serial.read(2), byteorder="big")
                    byte_count = int.from_bytes(self._serial.read(2), byteorder="big")
                    values = []
                    for i in range(byte_count):
                        values.append(int.from_bytes(self._serial.read(1), byteorder="big"))
                    response = response_frames.write_multiple_coils(start_address,quantity,values)
                    self._serial.write(response)

                elif(function_code == fc.write_multiple_registers):
                    start_address = int.from_bytes(self._serial.read(2), byteorder="big")
                    quantity = int.from_bytes(self._serial.read(2), byteorder="big")
                    byte_count = int.from_bytes(self._serial.read(2), byteorder="big")
                    values = []
                    for i in range(byte_count):
                        values.append(int.from_bytes(self._serial.read(1), byteorder="big"))
                    response = response_frames.write_multiple_registers(start_address,quantity,values)
                    self._serial.write(response)
        
        except TimeoutError:
            pass
    
    def run(self):
        while True:
            self.check_for_requests()
            