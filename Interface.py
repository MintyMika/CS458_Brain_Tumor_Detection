import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

def open_folder():
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        jpg_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg'))]
        total_images = len(jpg_files)
        
        if total_images == 0:
            progress_label.config(text="No .jpg images found in the selected folder")
        else:
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
                        
                        progress_label.config(text=f"Scanning {i}/{total_images} images")
                        root.update_idletasks()  # Update the display
                    
                    progress_label.config(text=f"All the images are successfully uploaded to the folder")

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

# Create a button to open a folder
open_button = tk.Button(root, text="Select the Folder to Scan", command=open_folder)
open_button.pack()

# Create a label for displaying progress
progress_label = tk.Label(root, text="", font=("Arial", 12))
progress_label.pack()

# Import the simpledialog module
from tkinter import simpledialog

# Run the Tkinter main loop
root.mainloop()