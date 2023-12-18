import zipfile
import os

def unzip_folder(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

# Example usage:
zip_file_path = r"C:\Users\DittmanSeon\Downloads\120523.zip"
extract_to_path = r"C:\Users\DittmanSeon\PycharmProjects\mri"

unzip_folder(zip_file_path, extract_to_path)
