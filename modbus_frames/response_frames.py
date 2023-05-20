from modbus_frames import functions_codes as fc

class ResponseFrames:
    _coils = []
    _discrete_inputs = []
    _holding_registers = []
    _input_registers = []
    
    def __init__(self,coils,discrete_inputs,holding_registers,input_registers):
        self._coils = coils
        self._discrete_inputs = discrete_inputs
        self._holding_registers = holding_registers
        self._input_registers = input_registers
    
    def read_coils(self,start_address,quantity):
        frame = bytearray()
        function_code = fc.read_coils
        frame.append(function_code)
        byte_count = quantity // 8 + (1 if quantity % 8 else 0)
        print(type(byte_count))
        frame += byte_count.to_bytes(2, byteorder='big')
        for i in range(byte_count):
            byte = 0
            for j in range(8):
                if self._coils[start_address + i * 8 + j]:
                    byte |= 1 << j
            frame += byte.to_bytes(1, byteorder='big')
        return frame
    
    def read_discrete_inputs(self,start_address,quantity):
        frame = bytearray()
        function_code = fc.read_discrete_inputs
        frame.append(function_code)
        byte_count = quantity // 8 + (1 if quantity % 8 else 0)
        frame += byte_count.to_bytes(2, byteorder='big')
        for i in range(byte_count):
            byte = 0
            for j in range(8):
                if self._discrete_inputs[start_address + i * 8 + j]:
                    byte |= 1 << j
            frame += byte.to_bytes(1, byteorder='big')
        return frame
    
    def read_holding_registers(self,start_address,quantity):
        frame = bytearray()
        function_code = fc.read_holding_registers
        frame.append(function_code)
        byte_count = quantity * 2
        frame += byte_count.to_bytes(2, byteorder='big')
        for i in range(quantity):
            frame += self._holding_registers[start_address + i].to_bytes(2, byteorder='big')
        return frame
    
    def read_input_registers(self,start_address,quantity):
        frame = bytearray()
        function_code = fc.read_input_registers
        frame.append(function_code)
        byte_count = quantity * 2
        frame += byte_count.to_bytes(2, byteorder='big')
        for i in range(quantity):
            frame += self._input_registers[start_address + i].to_bytes(2, byteorder='big')
        return frame

    def write_single_coil(self,address,value):
        frame = bytearray()
        function_code = fc.write_single_coil
        frame.append(function_code)
        frame += address.to_bytes(2, byteorder='big')
        if value == 0xFF00:
            self._coils[address] = True
        else:
            self._coils[address] = False
        frame += (0xFF00 if self._coils[address] else 0x0000).to_bytes(2, byteorder='big')
        return frame



def write_single_register(self,address,value):
    frame = bytearray()
    function_code = fc.write_single_register
    frame.append(function_code)
    frame += address.to_bytes(2, byteorder='big')
    self._holding_registers[address] = value
    frame += self._holding_registers[address].to_bytes(2, byteorder='big')
    return frame

def write_multiple_coils(self,start_address,quantity,values):
    frame = bytearray()
    function_code = fc.write_multiple_coils
    frame.append(function_code)
    frame += start_address.to_bytes(2, byteorder='big')
    frame += quantity.to_bytes(2, byteorder='big')
    byte_count = quantity // 8 + (1 if quantity % 8 else 0)
    frame += byte_count.to_bytes(1, byteorder='big')
    return frame

def write_multiple_registers(self,start_address,quantity,values):
    frame = bytearray()
    function_code = fc.write_multiple_registers
    frame.append(function_code)
    frame += start_address.to_bytes(2, byteorder='big')
    frame += quantity.to_bytes(2, byteorder='big')
    byte_count = quantity * 2
    frame += byte_count.to_bytes(1, byteorder='big')
    return frame