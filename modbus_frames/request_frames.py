import functions_codes as fc
def read_coils(start_address,quantity):
    """
    Function to build a read coils request frame
    """
    frame = bytearray()
    # Function code 
    function_code = fc.read_coils
    frame.append(function_code)
    # Start address
    frame += start_address.to_bytes(2, byteorder='big')
    # Quantity
    frame += quantity.to_bytes(2, byteorder='big')
    return frame

def read_discrete_inputs(start_address,quantity):
    """
    Function to build a read discrete inputs request frame
    """
    frame = bytearray()
    # Function code 
    function_code = fc.read_discrete_inputs
    frame.append(function_code)
    # Start address
    frame += start_address.to_bytes(2, byteorder='big')
    # Quantity
    frame += quantity.to_bytes(2, byteorder='big')
    return frame

def read_holding_registers(start_address,quantity):
    """
    Function to build a read holding registers request frame
    """
    frame = bytearray()
    # Function code 
    function_code = fc.read_holding_registers
    frame.append(function_code)
    # Start address
    frame += start_address.to_bytes(2, byteorder='big')
    # Quantity
    frame += quantity.to_bytes(2, byteorder='big')
    return frame

def read_input_registers(start_address,quantity):
    """
    Function to build a read input registers request frame
    """
    frame = bytearray()
    # Function code 
    function_code = fc.read_input_registers
    frame.append(function_code)
    # Start address
    frame += start_address.to_bytes(2, byteorder='big')
    # Quantity
    frame += quantity.to_bytes(2, byteorder='big')
    return frame

def write_single_coil(address,value):
    """
    Function to build a write single coil request frame
    """
    frame = bytearray()
    # Function code 
    function_code = fc.write_single_coil
    frame.append(function_code)
    # Address
    frame += address.to_bytes(2, byteorder='big')
    # Value
    frame += value.to_bytes(2, byteorder='big')
    return frame

def write_single_register(address,value):
    """
    Function to build a write single register request frame
    """
    frame = bytearray()
    # Function code 
    function_code = fc.write_single_register
    frame.append(function_code)
    # Address
    frame += address.to_bytes(2, byteorder='big')
    # Value
    frame += value.to_bytes(2, byteorder='big')
    return frame

def write_multiple_coils(start_address,quantity,values):
    """
    Function to build a write multiple coils request frame
    """
    frame = bytearray()
    # Function code 
    function_code = fc.write_multiple_coils
    frame.append(function_code)
    # Start address
    frame += start_address.to_bytes(2, byteorder='big')
    # Quantity
    frame += quantity.to_bytes(2, byteorder='big')
    # Byte count
    byte_count = len(values) // 8 +   bool(len(values) % 8)
    frame += byte_count.to_bytes(1, byteorder='big')
    # Values
    values = [bool(value) for value in values]
    for i in range(byte_count):
        byte = 0
        for j in range(7,-1,-1):
            try:
                byte += values[i*8+j] << j
            except IndexError:
                break
        frame += byte.to_bytes(1, byteorder='big')
    return frame
    
def write_multiple_registers(start_address,quantity,values):
    """
    Function to build a write multiple registers request frame
    """
    frame = bytearray()
    # Function code 
    function_code = fc.write_multiple_registers
    frame.append(function_code)
    # Start address
    frame += start_address.to_bytes(2, byteorder='big')
    # Quantity
    frame += quantity.to_bytes(2, byteorder='big')
    # Byte count
    byte_count = 2*quantity
    frame += byte_count.to_bytes(1, byteorder='big')
    # Values
    for value in values:
        frame += values.to_bytes(2, byteorder='big')
    return frame
