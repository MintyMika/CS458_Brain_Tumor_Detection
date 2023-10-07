import os

def check_folder_contents(folder_path):
    # Get a list of files in the folder
    folder_contents = os.listdir(folder_path)
    
    # Iterate through the files and check their extensions
    for file in folder_contents:
        _, file_extension = os.path.splitext(file)
        file_extension = file_extension.lower()
        
        if file_extension not in ['.jpg', '.jpeg']:
            print(f"Invalid file extension for file: {file}")

# Specify the folder path
folder_path = 'C:\\Users\\corneliuss2146\\Documents\\School Stuff\\Capstone\\Images test' # Change this later to whatever the file path is

# Check the folder contents for valid extensions
check_folder_contents(folder_path)
