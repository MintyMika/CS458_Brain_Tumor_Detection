# The code in this file will zip the folder

import os
import zipfile

def zipFolder(folder_path):
    # First get the name of the folder
    folder_name = os.path.basename(folder_path)
    # Now zip the folder
    zip_path = folder_path + '.zip'
    zip_file = zipfile.ZipFile(zip_path, 'w')
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            zip_file.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(folder_path, '..')))
    zip_file.close()

    # Make sure the zip file was created
    if os.path.exists(zip_path):
        print('Zip file created successfully')
    else:
        print('Zip file not created')

    return zip_path

#Debugging
folder_path = r'C:\Users\corneliuss2146\OneDrive - University of Wisconsin-Stout\Desktop\Work\JPEGs'
zip_path = zipFolder(folder_path)
print(zip_path)