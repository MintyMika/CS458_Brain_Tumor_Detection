import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2
from tkinter import filedialog
from PIL import Image, ImageTk
import pydicom as dicom
import shutil
import os

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    # You can add logic here to verify the username and password
    # For now, let's set a default login for testing
    if username == "test" and password == "test":
        login_window.destroy()  
        show_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to show the main window
def show_main_window():
    # Create the main window
    root = tk.Tk()
    root.title("Image Uploader")

    # Calculate the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the window size
    window_width = 400
    window_height = 400  

    # Calculate the window's position to center it on the screen
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the window size and position
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a label widget to display the message
    message_label = tk.Label(root, text="Brain Cancer Detector", font=("Arial", 14))
    message_label.pack(pady=10)

    # Create buttons to open a folder or a single file
    folder_button = tk.Button(root, text="Scan Folder", command=lambda: open_folder(root))
    folder_button.pack()

    file_button = tk.Button(root, text="Scan Single File", command=lambda: open_file(root))
    file_button.pack()

    # Create a label for displaying progress
    global progress_label
    progress_label = tk.Label(root, text="", font=("Arial", 12))
    progress_label.pack()

    # Run the Tkinter main loop
    root.mainloop()

def open_folder(root):
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        jpg_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg'))]
        dcm_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.dcm'))]
        total_dcm_images = len(dcm_files)

        if total_dcm_images > 0:
            for n, image in enumerate(dcm_files):
                ds = dicom.dcmread(os.path.join(folder_path, image))
                pixel_array_numpy = ds.pixel_array
                image = image.replace('.dcm', '.jpg')
                jpg_files.append(image)
            progress_label.config(text="Successfully converted .dcm files to .jpg images")        

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
                            image = Image.open(file_path)
                            
                            # Construct the output file path
                            output_path = os.path.join(custom_output_folder, file_name)
                            
                            # Save the image to the chosen folder
                            image.save(output_path)
                            
                            progress_label.config(text=f"Scanning {i}/{total_images} images", fg="green")
                            root.update_idletasks() 
                        
                        progress_label.config(text=f"All the images are successfully uploaded to the folder", fg="green")
            elif choice and choice.lower() == "existing":
                # Ask the user to select an existing folder as the output folder
                output_folder = filedialog.askdirectory(title="Select Existing Output Folder")
                
                if output_folder:
                    for i, file_name in enumerate(jpg_files, start=1):
                        file_path = os.path.join(folder_path, file_name)
                        
                        # Construct the output file path
                        output_path = os.path.join(output_folder, file_name)
                        
                        # Copy the image to the chosen folder
                        shutil.copy(file_path, output_path)
                        
                        progress_label.config(text=f"Scanning {i}/{total_images} images", fg="green")
                        root.update_idletasks()  
                    
                    progress_label.config(text=f"All the images are successfully uploaded to the folder", fg="green")
            else:
                progress_label.config(text="Invalid choice. Enter 'custom' or 'existing'.", fg="red")

def open_file(root):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg")])
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
                    
                    # Get the filename from the path and construct the output file path
                    file_name = os.path.basename(file_path)
                    output_path = os.path.join(custom_output_folder, file_name)
                    
                    # Save the image to the chosen folder
                    image.save(output_path)
                    
                    progress_label.config(text="The image is successfully uploaded to the folder", fg="green")
        elif choice and choice.lower() == "existing":
            # Ask the user to select an existing folder as the output folder
            output_folder = filedialog.askdirectory(title="Select Existing Output Folder")
            
            if output_folder:
                # Get the filename from the path and construct the output file path
                file_name = os.path.basename(file_path)
                output_path = os.path.join(output_folder, file_name)
                
                # Copy the image to the chosen folder
                shutil.copy(file_path, output_path)
                
                progress_label.config(text="The image is successfully uploaded to the folder", fg="green")
        else:
            progress_label.config(text="Invalid choice. Enter 'custom' or 'existing'.", fg="red")

# Create the login window
login_window = tk.Tk()
login_window.title("Login")

# Create labels and entry fields for username and password
username_label = tk.Label(login_window, text="Username:")
username_label.pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

password_label = tk.Label(login_window, text="Password:")
password_label.pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

# Create a login button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack()

# Run the login window
login_window.mainloop()