import socket
import os
import time
import sys

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
# server_address = ('69.23.75.181', 54321) # Uncomment this line to use the server's IP address

# Bind the socket to the server address and port
try:
    server_socket.bind(('192.168.0.63', 54321))
except socket.error as e:
    print(str(e))
    try:
        server_socket.bind(server_address)
    except socket.error as e:
        print(str(e))
        print("Failed to bind to server address and port")
        sys.exit()



# Listen for incoming connections
server_socket.listen(1)
print('Server is listening for incoming connections...')

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Received connection from:', client_address)

    # Receive the image data
    image_data = b''
    # Get the name of the file
    file_name = client_socket.recv(1024).decode()
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        image_data += data

    # Save the received image
    image_path = 'received_image.jpg'
    with open(file_name, 'wb') as file:
        file.write(image_data)
    print('Image saved as:', file_name)

    # Close the client connection
    client_socket.close()
