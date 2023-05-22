def crc(data):
    ''' takes byte array as input and returns 2 Byte crc in little endian '''
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for i in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, byteorder="little")
