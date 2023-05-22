from modbus_frames import request_frames
from modbus_frames import functions_codes as fc
from modbus_rtu import crc
from serial import Serial


class ModbusRtuClient():
    def __init__(self,server_address, port, baudrate, timeout):
        self._server_address = server_address
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout

    def read_coils(self,start_address,quantity):
        request_adu = self._server_address.to_bytes(1,byteorder='big')
        request_pdu = request_frames.read_coils(start_address,quantity)
        request_adu += request_pdu
        request_adu += crc.crc(request_adu)
        self._serial = Serial(self._port,baudrate=self._baudrate,timeout=self._timeout)
        self._serial.write(request_adu)
        byte_count = quantity//8 + (1 if quantity%8 else 0)
        response = self._serial.read( 5 + byte_count)
        if (crc.crc(response[:-2]) != response[-2:]):
            print(" CRC is not zero, discarding packets")
            return response
        if (response[0] != self._server_address):
            print("Server address doesn't match")
            return None
        if (response[1] != fc.read_coils):
            print("function code doesn't match")
            return None
        if (response[2] != byte_count):
            print(" Wrong Byte count")
            return None
        values = []
        data = response[3:-2]
        for byt_e,byte_no in zip(data,range(len(data))):
            for bit in range(0,8):
                if (quantity >= byte_no*8 + bit + 1):
                    values.append( (byt_e & 2**bit) >> bit )
        return values
    
    def read_discrete_inputs(self,start_address,quantity):
        request_adu = self._server_address.to_bytes(1,byteorder='big')
        request_pdu = request_frames.read_discrete_inputs(start_address,quantity)
        request_adu += request_pdu
        request_adu += crc.crc(request_adu)
        self._serial = Serial(self._port,baudrate=self._baudrate,timeout=self._timeout)
        self._serial.write(request_adu)
        byte_count = quantity//8 + (1 if quantity%8 else 0)
        response = self._serial.read( 5 + byte_count)
        if (crc.crc(response[:-2]) != response[-2:]):
            print(" CRC is not zero, discarding packets")
            return response
        if (response[0] != self._server_address):
            print("Server address doesn't match")
            return None
        if (response[1] != fc.read_discrete_inputs):
            print("function code doesn't match")
            return None
        if (response[2] != byte_count):
            print(" Wrong Byte count")
            return None
        values = []
        data = response[3:-2]
        for byt_e,byte_no in zip(data,range(len(data))):
            for bit in range(0,8):
                if (quantity >= byte_no*8 + bit + 1):
                    values.append( (byt_e & 2**bit) >> bit )
        return values
    

    def read_holding_registers(self,start_address,quantity):
        request_adu = self._server_address.to_bytes(1,byteorder='big')
        request_pdu = request_frames.read_holding_registers(start_address,quantity)
        request_adu += request_pdu
        request_adu += crc.crc(request_adu)
        self._serial = Serial(self._port,baudrate=self._baudrate,timeout=self._timeout)
        self._serial.write(request_adu)
        byte_count = 2*quantity
        response = self._serial.read( 5 + byte_count)
        if (crc.crc(response[:-2]) != response[-2:]):
            print(" CRC is not zero, discarding packets")
            return response
        if (response[0] != self._server_address):
            print("Server address doesn't match")
            return None
        if (response[1] != fc.read_holding_registers):
            print("function code doesn't match")
            return None
        if (response[2] != byte_count):
            print(" Wrong Byte count")
            return None
        values = []
        data = response[3:-2]
        for register_no in range(len(quantity)):
            value = (data[2*register_no]<<8) + data[2*register_no + 1]
            values.append(value)
            
        return values
    
    def read_input_registers(self,start_address,quantity):
        request_adu = self._server_address.to_bytes(1,byteorder='big')
        request_pdu = request_frames.read_input_registers(start_address,quantity)
        request_adu += request_pdu
        request_adu += crc.crc(request_adu)
        self._serial = Serial(self._port,baudrate=self._baudrate,timeout=self._timeout)
        self._serial.write(request_adu)
        byte_count = 2*quantity
        response = self._serial.read( 5 + byte_count)
        if (crc.crc(response[:-2]) != response[-2:]):
            print(" CRC is not zero, discarding packets")
            return response
        if (response[0] != self._server_address):
            print("Server address doesn't match")
            return None
        if (response[1] != fc.read_holding_registers):
            print("function code doesn't match")
            return None
        if (response[2] != byte_count):
            print(" Wrong Byte count")
            return None
        values = []
        data = response[3:-2]
        for register_no in range(len(quantity)):
            value = (data[2*register_no]<<8) + data[2*register_no + 1]
            values.append(value)
            
        return values

    def write_single_coil(self,address,value):
        request_adu = self._server_address.to_bytes(1,byteorder='big')
        request_pdu = request_frames.write_single_coil(address,value)
        request_adu += request_pdu
        request_adu += crc.crc(request_adu)
        self._serial = Serial(self._port,baudrate=self._baudrate,timeout=self._timeout)
        self._serial.write(request_adu)
        response = self._serial.read(8)
        if (crc.crc(response[:-2]) != response[-2:]):
            print(" CRC is not zero, discarding packets")
            return False
        if (response[0] != self._server_address):
            print("Server address doesn't match")
            return False
        if (response[1] != fc.write_single_coil):
            print("Invalid function code recieved")
            return False
        if ((response[2]<<8 + response[3]) != address):
            print("Invalid coil address recieved")
            return False
        if (value):
            if ( not (response[4] == 0xFF and response[5] == 0x00) ):
                print("Invalid value recieved")
                return False
        elif ( not (response[4] == 0x00 and response[5] == 0x00) ):
                print("Invalid value recieved")
                return False
        return True
    
    def write_single_register(self,address,value):
        request_adu = self._server_address.to_bytes(1,byteorder='big')
        request_pdu = request_frames.write_single_register(address,value)
        request_adu += request_pdu
        request_adu += crc.crc(request_adu)
        self._serial = Serial(self._port,baudrate=self._baudrate,timeout=self._timeout)
        self._serial.write(request_adu)
        response = self._serial.read(8)
        if (crc.crc(response[:-2]) != response[-2:]):
            print(" CRC is not zero, discarding packets")
            return False
        if (response[0] != self._server_address):
            print("Server address doesn't match")
            return False
        if (response[1] != fc.write_single_register):
            print("Invalid function code recieved")
            return False
        if ((response[2]<<8 + response[3]) != address):
            print("Invalid register address recieved")
            return False
        if ((response[4]<<8 + response[5]) != value):
            print("Invalid value recieved")
            return False
        return True
    
    def write_multiple_coils(self,start_address,quantity,values):
        request_adu = self._server_address.to_bytes(1,byteorder='big')
        request_pdu = request_frames.write_multiple_coils(start_address,quantity,values)
        request_adu += request_pdu
        request_adu += crc.crc(request_adu)
        self._serial = Serial(self._port,baudrate=self._baudrate,timeout=self._timeout)
        self._serial.write(request_adu)
        response = self._serial.read(8)
        if (crc.crc(response[:-2]) != response[-2:]):
            print(" CRC is not zero, discarding packets")
            return False
        if (response[0] != self._server_address):
            print("Server address doesn't match")
            return False
        if (response[1] != fc.write_multiple_registers):
            print("Invalid function code recieved")
            return False
        if ((response[2]<<8 + response[3]) != start_address):
            print("Invalid register address recieved")
            return False
        if ((response[4]<<8 + response[5]) != quantity):
            print("Invalid quantity recieved")
            return False
        return True
    

    def write_multiple_coils(self,start_address,quantity,values):
        request_adu = self._server_address.to_bytes(1,byteorder='big')
        request_pdu = request_frames.write_multiple_registers(start_address,quantity,values)
        request_adu += request_pdu
        request_adu += crc.crc(request_adu)
        self._serial = Serial(self._port,baudrate=self._baudrate,timeout=self._timeout)
        self._serial.write(request_adu)
        response = self._serial.read(8)
        if (crc.crc(response[:-2]) != response[-2:]):
            print(" CRC is not zero, discarding packets")
            return False
        if (response[0] != self._server_address):
            print("Server address doesn't match")
            return False
        if (response[1] != fc.write_multiple_registers):
            print("Invalid function code recieved")
            return False
        if ((response[2]<<8 + response[3]) != start_address):
            print("Invalid register address recieved")
            return False
        if ((response[4]<<8 + response[5]) != quantity):
            print("Invalid quantity recieved")
            return False
        return True


    


    


