import tkinter as tk
import cv2
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import pydicom as dicom
import shutil
import os

def open_folder_or_file():
    # Ask the user whether to upload a folder or a single file
    choice = simpledialog.askstring("Select Option", "Enter 'folder' to scan a folder or 'file' to scan a single file:")
    
    if choice and choice.lower() == "folder":
        open_folder()
    elif choice and choice.lower() == "file":
        open_file()
    else:
        progress_label.config(text="Invalid choice. Enter 'folder' or 'file'.", fg="red")

def open_folder():
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        jpg_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.dcm'))]

        progress_label.config(text="Successfully converted .dcm files to .jpg files")        

        total_images = len(jpg_files)
        
        if total_images == 0:
            progress_label.config(text="No .jpg images found in the selected folder", fg="red")
        else:
            # Ask the user whether to enter a custom folder name or select an existing folder
            choice = simpledialog.askstring("Select Option", "Enter 'custom' to enter a custom folder name or 'existing' to select an existing folder:")
            
            if choice and choice.lower() == "custom":
                # Prompt the user to enter a folder name
                custom_folder_name = simpledialog.askstring("Custom Folder Name", "Enter the name of the output folder:")
                
                if custom_folder_name:
                    # Ask the user to choose the output folder
                    output_folder = filedialog.askdirectory(title="Select Output Folder")
                    
                    if output_folder:
                        # Create the custom output folder
                        custom_output_folder = os.path.join(output_folder, custom_folder_name)
                        os.makedirs(custom_output_folder, exist_ok=True)
                        
                        for i, file_name in enumerate(jpg_files, start=1):
                            file_path = os.path.join(folder_path, file_name)

                            if (file_path.lower().endswith('.dcm')):
                                # Load dcm image
                                dicom_image = dicom.dcmread(file_path)

                                # convert dcm to jpg
                                jpg_image = Image.fromarray(dicom_image.pixel_array)

                                # convert jpg image to rgb mode
                                rgb_image = jpg_image.convert('RGB')

                                # construct file path for jpg image
                                jpg_filename = os.path.splitext(os.path.basename(file_name))[0] + '.jpg'
                                jpg_output_path = os.path.join(custom_output_folder, jpg_filename)

                                # save jpg image
                                rgb_image.save(jpg_output_path)
                            else:
                                # copy already-existing jpg image to output folder
                                output_path = os.path.join(custom_output_folder, file_name)
                                shutil.copy(file_path, output_path)
                            
                            progress_label.config(text=f"Scanning {i}/{total_images} images", fg="green")
                            root.update_idletasks()  # Update the display
                        
                        progress_label.config(text=f"All the images are successfully uploaded to the folder", fg="green")
            elif choice and choice.lower() == "existing":
                # Ask the user to select an existing folder as the output folder
                output_folder = filedialog.askdirectory(title="Select Existing Output Folder")
                
                if output_folder:
                    for i, file_name in enumerate(jpg_files, start=1):
                        file_path = os.path.join(folder_path, file_name)
                        
                        if(file_path.lower().endswith('.dcm')):
                            # #Load dcm image
                            dicom_image = dicom.dcmread(file_path)
                            
                            # convert dcm to jpg
                            jpg_image = Image.fromarray(dicom_image.pixel_array)

                            # convert jpg image to rgb mode
                            rgb_image = jpg_image.convert('RGB')
                            
                            # construct file path for jpg image
                            jpg_filename = os.path.splitext(os.path.basename(file_name))[0] + '.jpg'
                            jpg_output_path = os.path.join(output_folder, jpg_filename)
                            
                            # save jpg image
                            rgb_image.save(jpg_output_path)
                        else:
                            # copy already-existing jpg image to output folder
                            output_path = os.path.join(output_folder, file_name)
                            shutil.copy(file_path, output_path)
                        
                        progress_label.config(text=f"Scanning {i}/{total_images} images", fg="green")
                        root.update_idletasks()  # Update the display
                    
                    progress_label.config(text=f"All the images are successfully uploaded to the folder", fg="green")
            else:
                progress_label.config(text="Invalid choice. Enter 'custom' or 'existing'.", fg="red")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg, *.dcm")])
    if file_path:
        image = Image.open(file_path)
        
        # Ask the user whether to enter a custom folder name or select an existing folder
        choice = simpledialog.askstring("Output Folder", "Enter 'custom' to enter a custom folder name or 'existing' to select an existing folder:")
        
        if choice and choice.lower() == "custom":
            # Prompt the user to enter a folder name
            custom_folder_name = simpledialog.askstring("Custom Folder Name", "Enter the name of the output folder:")
            
            if custom_folder_name:
                # Ask the user to choose the output folder
                output_folder = filedialog.askdirectory(title="Select Output Folder")
                
                if output_folder:
                    # Create the custom output folder
                    custom_output_folder = os.path.join(output_folder, custom_folder_name)
                    os.makedirs(custom_output_folder, exist_ok=True)
                    if (file_path.lower().endswith('.dcm')):
                        # Load dcm image
                        dicom_image = dicom.dcmread(file_path)

                        # convert dcm to jpg
                        jpg_image = Image.fromarray(dicom_image.pixel_array)

                        # convert jpg image to rgb mode
                        rgb_image = jpg_image.convert('RGB')

                        # construct file path for jpg image
                        jpg_filename = os.path.splitext(os.path.basename(file_name))[0] + '.jpg'
                        jpg_output_path = os.path.join(custom_output_folder, jpg_filename)

                        # save jpg image
                        rgb_image.save(jpg_output_path)
                    else:
                        # copy already-existing jpg image to output folder
                        output_path = os.path.join(custom_output_folder, file_name)
                        shutil.copy(file_path, output_path)
                    
                    progress_label.config(text="The image is successfully uploaded to the folder", fg="green")
        elif choice and choice.lower() == "existing":
            # Ask the user to select an existing folder as the output folder
            output_folder = filedialog.askdirectory(title="Select Existing Output Folder")
            
            if output_folder:
                # Get the filename from the path and construct the output file path
                file_name = os.path.basename(file_path)
                output_path = os.path.join(output_folder, file_name)
                
                if(file_path.lower().endswith('.dcm')):
                    # #Load dcm image
                    dicom_image = dicom.dcmread(file_path)
                            
                    # convert dcm to jpg
                    jpg_image = Image.fromarray(dicom_image.pixel_array)

                    # convert jpg image to rgb mode
                    rgb_image = jpg_image.convert('RGB')
                            
                    # construct file path for jpg image
                    jpg_filename = os.path.splitext(os.path.basename(file_name))[0] + '.jpg'
                    jpg_output_path = os.path.join(output_folder, jpg_filename)
                            
                    # save jpg image
                    rgb_image.save(jpg_output_path)
                else:
                    # copy already-existing jpg image to output folder
                    output_path = os.path.join(output_folder, file_name)
                    shutil.copy(file_path, output_path)
                
                progress_label.config(text="The image is successfully uploaded to the folder", fg="green")
        else:
            progress_label.config(text="Invalid choice. Enter 'custom' or 'existing'.", fg="red")

# Create the main window
root = tk.Tk()
root.title("Image Uploader")

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size
window_width = 400
window_height = 400  # Increased the height for the progress message

# Calculate the window's position to center it on the screen
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a label widget to display the message
message_label = tk.Label(root, text="Brain Cancer Detector", font=("Arial", 14))
message_label.pack(pady=10)

# Create buttons to open a folder or a single file
folder_button = tk.Button(root, text="Scan Folder", command=open_folder)
folder_button.pack()

file_button = tk.Button(root, text="Scan Single File", command=open_file)
file_button.pack()

# Create a label for displaying progress
progress_label = tk.Label(root, text="", font=("Arial", 12))
progress_label.pack()

# Run the Tkinter main loop
root.mainloop()