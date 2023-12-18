import socket
import os
import time
import sys
import MLModel as ML
import MLAverage as MLA
import Unzip
import DatabaseFuncs as DB


# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
# server_address = ('69.23.75.181', 54321) # Uncomment this line to use the server's IP address

# Bind the socket to the server address and port
try:
    server_socket.bind(('192.168.0.64', 54321))
except socket.error as e:
    print(str(e))
    
    try:
            server_socket.bind(server_socket.getsockname()[0], 54321)
    except socket.error as e:
            print(str(e))
            print("Failed to bind to server address and port")
            sys.exit()



# Listen for incoming connections
server_socket.listen(1)
print('Server is listening for incoming connections...')

while True:
    # 1. Listening for incoming connections
    # 2. Accepting incoming connections
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Received connection from:', client_address)
    
    file_data = b'' # The data of the file

    # Get the name of the username, userID, and file
    try:
        # username = client_socket.recv(1024).decode()
        userID = client_socket.recv(1024).decode('utf-8')
        print("userID: "+ userID)
        # Send a confirmation message to the client
        client_socket.sendall("Received userID".encode())

        file_name = client_socket.recv(1024).decode('utf-8')
        print("File name: " + file_name)
        # Send a confirmation message to the client
        client_socket.sendall("Received file name".encode())
        
        # file_size = client_socket.recv(1024)
        # file_size = int.from_bytes(file_size, "big")
        # print("File size: " + str(file_size))
    except Exception as e:
        print(e)
        break

    # 3. Receiving the file
    try:
         data = b''
         while True:
             data = client_socket.recv(1024)
             if not data:
                 break
             file_data += data
    except Exception as e:
        print(e)
        break

        

    

    # Save the received zip file
    with open(file_name, 'wb') as file:
        file.write(file_data)

    # Make sure the zip file isn't empty
    if os.path.getsize(file_name) == 0:
        print("Empty file")
        break
    


    # Save the received image
    # image_path = 'received_image.jpg'
        
    # If the file is zip, unzip it
    # 4. Unzipping the file
    if file_name.endswith(".zip"):
        # Unzip the file
        Unzip.unzip_file(file_name, r"C:\CapstoneImages")
        # Get the folder path
        folder_path = os.path.join(r"C:\CapstoneImages", file_name[:-4])
        # Get the results
        results = MLA.ML_nice_results(folder_path)
        # Get the averages
        average_results = MLA.ML_get_folder_averages(results)
        # Send the results back to the SQL server
        DB.update_user_result(userID, average_results)


        # Iterate through the unzipped folder, get the full path of each image and add it to the database
        for img_filename in os.listdir(folder_path):
            if img_filename.endswith(".jpg"):
                img_path = os.path.join(folder_path, img_filename) # Full path to the image
                print(img_path)
                # Add the image to the database
                DB.add_image_to_database(userID, img_path)

        # client_socket.sendall(str(average_results).encode())
    else:
        # Save the image
        with open(file_name, 'wb') as file:
            file.write(image_data)
        # Get the results
        results = ML.process_image(currImage=file_name)
        # Send the results back to the client
        client_socket.sendall(str(results).encode())

    # Close the client connection
    client_socket.close()
