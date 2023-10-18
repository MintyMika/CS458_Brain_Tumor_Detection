import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from PIL import Image, ImageTk
import pydicom as dicom
import shutil
import os
import matplotlib.pyplot as plt

# Function to convert dcm to jpg
def dcm_to_jpg(input, output):
    dcm_data = dicom.dcmread(input)
    pixel_array = dcm_data.pixel_array
    plt.imshow(pixel_array, cmap=plt.cm.bone)
    plt.axis('off')
    plt.savefig(output, bbox_inches='tight', pad_inches=0, dpi=300)

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username == "test" and password == "test":
        login_window.withdraw()  
        show_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def create_user():
    messagebox.showinfo("Create User", "Feature to create a new user is not implemented yet.")

def logout():
    main_window.destroy()  
    login_window.deiconify()  

def show_main_window():
    global main_window
    main_window = tk.Tk()
    main_window.title("Image Uploader")

    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()

    window_width = 400
    window_height = 400  

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    message_label = tk.Label(main_window, text="Brain Cancer Detector", font=("Arial", 14))
    message_label.pack(pady=10)

    folder_button = tk.Button(main_window, text="Scan Folder", command=lambda: open_folder(main_window))
    folder_button.pack()

    file_button = tk.Button(main_window, text="Scan Single File", command=lambda: open_file(main_window))
    file_button.pack()

    global progress_label
    progress_label = tk.Label(main_window, text="", font=("Arial", 12))
    progress_label.pack()

    logout_button = tk.Button(main_window, text="Log Out", command=logout)
    logout_button.pack()

    main_window.mainloop()

def open_folder(root):
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        jpg_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.dcm'))]          

        total_images = len(jpg_files)
        
        if total_images == 0:
            progress_label.config(text="No .jpg images found in the selected folder", fg="red")
        else:
            choice = simpledialog.askstring("Select Option", "Enter 'custom' to enter a custom folder name or 'existing' to select an existing folder:")
            
            if choice and choice.lower() == "custom":
                custom_folder_name = simpledialog.askstring("Custom Folder Name", "Enter the name of the output folder:")
                
                if custom_folder_name:
                    output_folder = filedialog.askdirectory(title="Select Output Folder")
                    
                    if output_folder:
                        custom_output_folder = os.path.join(output_folder, custom_folder_name)
                        os.makedirs(custom_output_folder, exist_ok=True)
                        
                        for i, file_name in enumerate(jpg_files, start=1):
                            file_path = os.path.join(folder_path, file_name)


                            if (file_path.lower().endswith('.dcm')):
                                # construct file path for jpg image
                                jpg_filename = os.path.splitext(os.path.basename(file_name))[0] + '.jpg'
                                jpg_output_path = os.path.join(custom_output_folder, jpg_filename)

                                # convert dcm to jpg
                                dcm_to_jpg(file_path, jpg_output_path)
                            else:
                                output_path = os.path.join(custom_output_folder, os.path.basename(file_path))
                                shutil.copy(file_path, output_path)
                            
                            progress_label.config(text=f"Scanning {i}/{total_images} images", fg="green")
                            root.update_idletasks() 
                        
                        progress_label.config(text=f"All the images are successfully uploaded to the folder", fg="green")
            elif choice and choice.lower() == "existing":
                output_folder = filedialog.askdirectory(title="Select Existing Output Folder")
                
                if output_folder:
                    for i, file_name in enumerate(jpg_files, start=1):
                        file_path = os.path.join(folder_path, file_name)
                        

                        if(file_path.lower().endswith('.dcm')):
                            # construct file path for jpg image
                            jpg_filename = os.path.splitext(os.path.basename(file_path))[0] + '.jpg'
                            jpg_output_path = os.path.join(output_folder, jpg_filename)

                            # convert dcm to jpg
                            dcm_to_jpg(file_path, jpg_output_path)
                        else:
                            output_path = os.path.join(output_folder, os.path.basename(file_path))
                            shutil.copy(file_path, output_path)
                        
                        progress_label.config(text=f"Scanning {i}/{total_images} images", fg="green")
                        root.update_idletasks()  
                    
                    progress_label.config(text=f"All the images are successfully uploaded to the folder", fg="green")
            else:
                progress_label.config(text="Invalid choice. Enter 'custom' or 'existing'.", fg="red")

def open_file(root):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.dcm")])
    
    if file_path:     
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
                        # construct file path for jpg image
                        jpg_filename = os.path.splitext(os.path.basename(file_path))[0] + '.jpg'
                        jpg_output_path = os.path.join(custom_output_folder, jpg_filename)

                        # convert dcm to jpg
                        dcm_to_jpg(file_path, jpg_output_path)
                    else:
                        # copy already-existing jpg image to output folder
                        output_path = os.path.join(custom_output_folder, os.path.basename(file_path))
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
                    # construct file path for jpg image
                    jpg_filename = os.path.splitext(os.path.basename(file_path))[0] + '.jpg'
                    jpg_output_path = os.path.join(output_folder, jpg_filename)

                    # convert dcm to jpg
                    dcm_to_jpg(file_path, jpg_output_path)
                else:
                    # copy already-existing jpg image to output folder
                    output_path = os.path.join(output_folder, os.path.basename(file_path))
                    shutil.copy(file_path, output_path)
                    progress_label.config(text="The image is successfully uploaded to the folder", fg="green")
            else:
                progress_label.config(text="Invalid choice. Enter 'custom' or 'existing'.", fg="red")

login_window = tk.Tk()
login_window.title("Login")

username_label = tk.Label(login_window, text="Username:")
username_label.pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

password_label = tk.Label(login_window, text="Password:")
password_label.pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

login_button = tk.Button(login_window, text="Login", command=login)
login_button.pack()

create_user_button = tk.Button(login_window, text="Create a User", command=create_user)
create_user_button.pack()

login_window.mainloop()