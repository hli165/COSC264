def FileRequest(file_name):
    """create header for file (Client)"""
    header = []
    total_MagicNo = 0x497E
    magicNo1 = total_MagicNo >> 8
    MagicNo2 = total_MagicNo & 0xFF
    Type = 0x1
    if len(file_name) < 1 or len(file_name) > 1024:
        print("ERROR: FILE NAME IS TOO LONG")
    else:
        total_FilenameLen = len(file_name)
        FilenameLen1 = total_FilenameLen >> 8
        FilenameLen2 = total_FilenameLen & 0xFF
    header.append(magicNo1)
    header.append(MagicNo2)
    header.append(Type)
    header.append(FilenameLen1)
    header.append(FilenameLen2)
    return bytearray(header) + bytearray(file_name)


def FileResponse_Reader(byte_array):
    """Decode the file response"""
    file_data = ''
    for character in byte_array:
        file_data += chr(character)
    return file_data
