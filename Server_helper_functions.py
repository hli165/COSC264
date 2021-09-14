import os
import socket
import datetime
import sys


def FileResponse(File_data, Status_code):
    """Create header for file (Server)"""
    Header = []
    if Status_code == 0:
        total_MagicNo = 0x497E
        magicNo1 = total_MagicNo >> 8
        MagicNo2 = total_MagicNo & 0xFF
        Type = 0x2
        Header.append(magicNo1)
        Header.append(MagicNo2)
        Header.append(Type)
        Header.append(Status_code)
        return bytearray(Header)
    else:
        total_MagicNo = 0x497E
        Type = 0x2
        total_File_data = len(File_data)
        magicNo1 = total_MagicNo >> 8
        MagicNo2 = total_MagicNo & 0xFF
        DataLength_byte1 = total_File_data >> 24
        DataLength_byte2 = (total_File_data >> 16) & 0xFF
        DataLength_byte3 = (total_File_data >> 8) & 0xFF
        DataLength_byte4 = total_File_data & 0xFF
        Header.append(magicNo1)
        Header.append(MagicNo2)
        Header.append(Type)
        Header.append(Status_code)
        Header.append(DataLength_byte1)
        Header.append(DataLength_byte2)
        Header.append(DataLength_byte3)
        Header.append(DataLength_byte4)
        return bytearray(Header) + bytearray(File_data)


def FileRequest_Reader(byte_array, Client):
    """Decode and determine a bytearray"""
    if (byte_array[0] << 8) + byte_array[1] != 0x497E:
        Client.close()
        print("ERROR: THE MAGIC NUMBER IS INCORRECT\n")
    elif byte_array[2] != 1:
        Client.close()
        print("THE TYPE IS INCORRECT\n")
    elif (byte_array[3] << 8) + byte_array[4] > 1024 or (byte_array[3] << 8) + byte_array[4] < 1:
        Client.close()
        print("THE FILE NAME LENGTH IS INCORRECT\n")
    else:
        File_name = ''
        for character in byte_array[5:]:
            File_name += chr(character)
        return File_name


def File_Sender(File_data, Status_Code):
    """send the requested file to client"""
    # File_data = ''
    # file = open(file_name, "rb")
    # File_data = file.read()
    # except Exception:
    #    Status_Code = 0
    #    print("THE REQUESTED FILE IS NOT EXIST")
    #    return -1
    File_response = FileResponse(File_data, Status_Code)
    print(Status_Code)
    print("{} BYTES HAS BEEN TRANSFERRED".format(len(File_response)))
    return File_response
