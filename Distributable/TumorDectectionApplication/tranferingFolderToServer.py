import socket
import os
import zippingFolder as zf


def sendZippedFolder(userID, folder_path):
    # Server details
    server_ip = '69.23.75.181'
    server_port = 54321

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    sock.connect((server_ip, server_port))

    # Zip the folder
    zip_path = zf.zipFolder(folder_path)
    old_zip_path = zip_path
    zip_size = os.path.getsize(zip_path)
    file_size_in_bytes = zip_size.to_bytes(1024, byteorder='big')


    # Send the userID and zip_path to the server
    sendinguserID = userID.encode('utf-8')
    
    # Get only the name of the zip file
    zip_path = os.path.basename(zip_path)
    print(zip_path)
    sendingFileName = zip_path.encode('utf-8')

    try:
        sock.send(sendinguserID)
        # recieve confirmation from server
        print(sock.recv(1024).decode())
        sock.send(sendingFileName)
        # recieve confirmation from server
        print(sock.recv(1024).decode())
        # sock.send(str(file_size_in_bytes).encode())
    except Exception as e:
        print(e)
        print('Error sending userID and zip_path to server')
        return

    # # Send the zip file to the server
    with open(old_zip_path, 'rb') as f:
        data = f.read(1024)
        while data:
            sock.send(data)
            data = f.read(1024)
    
    # Close the socket
    sock.close()

    # Delete the zip file
    os.remove(old_zip_path)

# Debugging
# userID = '1'
# folder_path = r'C:\Users\corneliuss2146\OneDrive - University of Wisconsin-Stout\Desktop\Work\JPEGs'
# sendZippedFolder(userID, folder_path)
