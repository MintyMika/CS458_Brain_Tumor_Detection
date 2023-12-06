import socket
import os
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('69.23.75.181', 54321)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print('Server is listening for incoming connections...')

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Received connection from:', client_address)

    # Receive the image data
    image_data = b''
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        image_data += data

    # Save the received image
    image_path = 'received_image.jpg'
    with open(image_path, 'wb') as file:
        file.write(image_data)
    print('Image saved as:', image_path)

    # Close the client connection
    client_socket.close()
