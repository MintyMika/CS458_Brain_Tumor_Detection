import socket
import os

# Server details
server_ip = '69.23.75.181'
server_port = 54321

# Image file path
image_path = 'C:\\Users\\corneliuss2146\\Documents\\Capstone\\FTP\\testimage.jpg'

# instead of sending just the image let's try sending the entire folder

folder_path = 'C:\\Users\\corneliuss2146\\Documents\\Capstone\\FTP\\testfolder'

# Read image file in binary mode
with open(image_path, 'rb') as file:
    image_data = file.read()

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))

# Send the name of the image file
client_socket.sendall(os.path.basename(image_path).encode())

# Send the image data through the socket
client_socket.sendall(image_data)

# Close the socket
client_socket.close()
import socket
