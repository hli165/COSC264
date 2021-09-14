
import socket
import datetime
import sys
from Server_helper_functions import *

def main():
    # Read port number from command line
    port_number = input("Select your port number (BETWEEN 1,024 AND 64,000)\n")
    try:
        port_number = int(port_number)
    except ValueError:
        print("ERROR: THE PORT NUMBER MUST BE AN INTEGER\n")
        sys.exit(1)

    # Check the port number is valid 
    if port_number < 1024 or port_number > 64000:
        print("ERROR: THE PORT NUMBER SHOULD BE BETWEEN 1,024 AND 64,000(INCLUDING)")
        sys.exit(1)
    else:
        print("PORT NUMBER SET WITH SUCCESS\n......")

    # Create a Socket Server
    try:
        TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("TCP SOCKET CREATED WITH SUCCESS\n......")
    except socket.error as creat_ERROR:
        sys.exit(1)

    # Check that socket is successfully bind
    try:
        TCP_socket.bind(("127.0.0.1", port_number))
        print("TCP SOCKET BIND WITH SUCCESS\n.......")
    except socket.error as bind_ERROR:
        sys.exit(1)

    # Put the socket into listening mode
    try:
        TCP_socket.listen(5)
        print("SOCKET IS LISTENING......")
    except socket.error as listen_ERROR:
        sys.exit(listen_ERROR)

    # The server enters an infinite loop
    # Unitil we interrupt it
    while True:
        try:
            Client, Client_addr = TCP_socket.accept()
            print("Got connection from {}. The port number is: {}".format(Client_addr, port_number)) #Print client's information 
            print("The current time is: {}".format(datetime.datetime.now().time()))
        except socket.error as accept_ERROR:
            print(accept_ERROR)
            continue

        # Receive FileRequest record from the connection 
        try:
            file_request = Client.recv(4096)
        except socket.timeout as time_ERROR:
            print("TIMEOUT")
            Client.close()
            continue

        # Read FileRequest
        # Check if header is correct and contains a filename       
        try:
            file_name = FileRequest_Reader(file_request, Client)
        except Exception:
            Client.close()
            continue
        
        # Server open the requested file for reading
        # Raise FileNotFoundError if the file is not exist in server
        try:
            File_data = ''
            Status_Code = 1
            file = open(file_name, "rb")
            File_data = file.read()
            file_response = File_Sender(File_data, Status_Code)
            file.close()
        except FileNotFoundError:
            print("THE REQUESTED FILE IS NOT EXIST IN SERVER")
            File_data = ''
            Status_Code = 0
            file_response = File_Sender(File_data.encode(), Status_Code)
            Client.send(file_response)
            Client.close()
            continue

        # Send FileResponse message back to the Client
        # Print an information which includes the actual number of bytes transfeered
        # Go back to the start of the loop, Server still listening...   
        try:
            Client.send(file_response)
        except socket.error as send_error:
            print(send_error)
            Client.close()
            continue


if __name__ == '__main__':
    main()