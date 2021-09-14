from Client_helper_functions import FileRequest, FileResponse_Reader
import socket
import sys
import math


def main():
    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creat a new socket


    IP_addr = input("PLEASE ENTER THE SERVER IP IN DOTTED-DECIMAL NOTATION OR ENTER THE HOSTNAME\n") #input IP address or the hostanme
    try:
        Ip_addr = socket.gethostbyname(IP_addr)  #Convert Hostname to IP address
    except socket.gaierror:
        print("INVALID IP ADDRESS")
        Client.close()
        sys.exit(1)

    # Input port number to connect to tthe server
    port_number = input("Select your port number (BETWEEN 1,024 AND 64,000)\n")
    try:
        port_number = int(port_number)
    except ValueError:
        print("ERROR: THE PORT NUMBER MUST BE AN INTEGER\n")
        Client.close()
        sys.exit(1)

    # Check the port number is vaild 
    if port_number < 1024 or port_number > 64000:
        print("ERROR: THE PORT NUMBER SHOULD BE BETWEEN 1,024 AND 64,000(INCLUDING)")
        Client.close()
        sys.exit(1)
    else:
        print("--------------------------------------")
        print("PORT NUMBER SET WITH SUCCESS")
        print("--------------------------------------")

    # Connect client to the server
    try:
        Client.connect((IP_addr, port_number))
        print("--------------------------------------")
        print("SUCCESSFUL CONNECT TO SOCKET")
        print("--------------------------------------")
    except socket.error as connect_ERROR:
        Client.close()
        sys.exit(connect_ERROR)

    # Input the file client wants to retrieve from the server
    file_name = input("PLEASE SELECT THE FILE YOU WANT TO RETRIEVE FROM THE SERVER\n")
    file_name_encode = file_name.encode('utf-8')
    try:
        packed_file = FileRequest(file_name_encode)
    except Exception:
        Client.close()
        sys.exit("error")

    # Send FileRequest to the server
    try:
        Client.send(packed_file)
        print("--------------------------------------")
        print("YOUR REQUEST HAS BEEN SEND TO THE SERVER")
        print("--------------------------------------")
    except socket.error as send_ERROR:
        Client.close()
        sys.exit(send_ERROR)

    # Receive the FileResponse Header from the server
    # Check if the Header is correct
    try:
        recv_Header = Client.recv(8)
    except socket.error as recv_ERROR:
        Client.close()
        sys.exit(recv_ERROR)

    if (recv_Header[0] << 8) + recv_Header[1] != 0x497E:
        Client.close()
        print("--------------------------------------")
        sys.exit("ERROR: THE MAGIC NUMBER IS INCORRECT\n")

    elif recv_Header[2] != 2:
        Client.close()
        print("--------------------------------------")
        sys.exit("THE TYPE IS INCORRECT\n")
    elif recv_Header[3] != 1:
        Client.close()
        print("--------------------------------------")
        sys.exit("SERVER WAS UNABLE TO OPEN THE REQUESTED FILE, THE FILE DES NOT EXIST ON THE SERVER OR THE SERVER WAS "
                 "NOT ABLE TO OPEN")
    else:
        dataLength = (recv_Header[4] << 24 | recv_Header[5] << 16 | recv_Header[6] << 8 | recv_Header[7])     # Find the dataLength 

    # Read the FileResponse without the Header, write blocks to the new file
    # Each block is up to 4096 bytes size
    # Count the number of bytes received from the server
    byte_Total = 0
    data = ''
    recv_Time = math.ceil(dataLength / 4096)
    for i in range(recv_Time):
        try:
            recv_Data = Client.recv(4096)
            Client.settimeout(1)
            byte_Total += len(recv_Data)
            data += FileResponse_Reader(recv_Data)
        except socket.error:
            Client.close()
            print("--------------------------------------")
            print("FAIL TO RECEIVE DATA")
            print("SOCKET IS CLOSED")
    try:
        if data:
            with open(file_name, "wb+") as f:
                f.write(bytearray(data.encode()))
                print("NEW FILE HAS BEEN UPLOADED")
                print("{} BYTES IS RECEIVED FROM THE SERVER".format(byte_Total))
    except FileExistsError:
        print("--------------------------------------")
        print("THE REQUESTED FILE IS ALREADY EXIST")
        Client.close()

 

if __name__ == '__main__':
    main()
