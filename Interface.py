import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from PIL import Image, ImageTk
from tkinter import PhotoImage
import pydicom as dicom
import shutil
import os
import mysql.connector
import hashlib
import matplotlib.pyplot as plt
import re
import random
import string
import smtplib
import base64
import requests
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from email.mime.text import MIMEText
from urllib.request import urlopen 
import requests
from io import BytesIO

# Create variables for entry fields
username_entry = None
password_entry = None
search_entry = None
search_button = None
search_results_listbox = None 

# Create global variables for user data
first_name = ""
last_name = ""
user_role = ""

# Create a global variable for the role selection
role_var = None

# Make search_results_listbox a global variable
search_results_listbox = None



def set_background_image(window, image_path):
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    # Create a Canvas widget to cover the entire window
    canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
    canvas.place(x=0, y=0, relwidth=1, relheight=1)  # Place at the bottom

    # Place the image on the Canvas
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    # Keep a reference to the image to prevent it from being garbage collected
    canvas.image = photo

    
# Function to convert dcm to jpg
def dcm_to_jpg(input, output):
    dcm_data = dicom.dcmread(input)
    pixel_array = dcm_data.pixel_array
    plt.imshow(pixel_array, cmap=plt.cm.bone)
    plt.axis('off')
    plt.savefig(output, bbox_inches='tight', pad_inches=0, dpi=300)

# Function to hash the password
def hashed_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed

#Function to verify if user already exist
def user_exists(username, first_name, last_name):
    db = mysql.connector.connect(
        host="69.23.75.181",
        user="CMAdmin",
        password="Chucky123",
        database="brain_cancer_mock_data"
    )
    cursor = db.cursor()

    # Check if a user with the provided first name, last name, and username already exists
    cursor.execute("SELECT COUNT(*) FROM user WHERE username = %s OR (firstName = %s AND lastName = %s)", (username, first_name, last_name))
    result = cursor.fetchone()
    user_count = result[0]

    cursor.close()
    db.close()

    return user_count > 0

#Function For the SearchBox in Doctor view
def search_patients(search_term):
    db = mysql.connector.connect(
        host="69.23.75.181",
        user="CMAdmin",
        password="Chucky123",
        database="brain_cancer_mock_data"
    )
    cursor = db.cursor()

    # Modify the query to filter patients based on the role
    cursor.execute("SELECT userId, firstName, lastName FROM user WHERE role = 'Patient' AND (firstName LIKE %s OR lastName LIKE %s)", ('%' + search_term + '%', '%' + search_term + '%'))

    results = cursor.fetchall()  # Fetch all results

    cursor.close()
    db.close()

    return results

#Function to display the SearchBox in Doctor view
def search_patients_and_display(search_term):
    results = search_patients(search_term)

    # Clear the previous search results
    search_results_listbox.delete(0, tk.END)

    if results:
        for result in results:
            full_name = f"{result[1]} {result[2]}"
            search_results_listbox.insert(tk.END, full_name)
    else:
        search_results_listbox.insert(tk.END, "No results found")

def login():
    global username_entry, password_entry, first_name, last_name, user_role

    username = username_entry.get()
    password = password_entry.get()
    
    # Set up MySQL connection 
    db = mysql.connector.connect(
        host="69.23.75.181",
        user="CMAdmin",
        password="Chucky123",
        database="brain_cancer_mock_data"
    )
    cursor = db.cursor()

    # Execute a SELECT query
    cursor.execute("SELECT userId, password, firstName, lastName, role FROM user WHERE username = %s", (username,))

    result = cursor.fetchone()  # Fetch the first result

    if result:
        # Verify the hashed password
        db_password = result[1]
        entered_password = hashed_password(password)

        if db_password == entered_password:
            first_name = result[2]
            last_name = result[3]
            user_role = result[4]
            login_window.withdraw()  
            show_main_window()
        else:
            messagebox.showerror("Login Failed", "Password does not match.")
    else:
        messagebox.showerror("Login Failed", "Username not found")

    cursor.close()
    db.close()

# Function to create service for sending email

def create_service():
    creds = Credentials.from_authorized_user_file('C:\\Users\\MasseyCharles\\OneDrive - University of Wisconsin-Stout\\Documents\\sesh 5\\Software Eng\\Project\\updated version\\CS458_Brain_Tumor_Detection\\token.json')
    scopes = ['https://www.googleapis.com/auth/gmail.send']
    creds = Credentials.from_authorized_user_file('C:\\Users\\MasseyCharles\\OneDrive - University of Wisconsin-Stout\\Documents\\sesh 5\\Software Eng\\Project\\updated version\\CS458_Brain_Tumor_Detection\\token.json', scopes=scopes)
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as error:
        print(f'An error occurred: {error}')

# Function to create the message itself
def create_message(sender, to, subject, message_text):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text)
    message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    return body

# Function to create a new user
def create_user():
    create_user_window = tk.Tk()
    create_user_window.title("Create User")
    create_user_window.geometry("400x400")
    create_user_window.resizable(False, False) 

    # Create and pack labels, entry widgets, and dropdown for user details
    first_name_label = tk.Label(create_user_window, text="First Name:")
    first_name_label.pack()
    first_name_entry = tk.Entry(create_user_window)
    first_name_entry.pack()

    last_name_label = tk.Label(create_user_window, text="Last Name:")
    last_name_label.pack()
    last_name_entry = tk.Entry(create_user_window)
    last_name_entry.pack()

    username_label = tk.Label(create_user_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(create_user_window)
    username_entry.pack()

    email_label = tk.Label(create_user_window, text="Email:")
    email_label.pack()
    email_entry = tk.Entry(create_user_window)
    email_entry.pack()

    password_label = tk.Label(create_user_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(create_user_window, show="*")
    password_entry.pack()

    # Add a password confirmation entry
    password_confirm_label = tk.Label(create_user_window, text="Confirm Password:")
    password_confirm_label.pack()
    password_confirm_entry = tk.Entry(create_user_window, show="*")
    password_confirm_entry.pack()

    dob_label = tk.Label(create_user_window, text="Date of Birth (yyyy-mm-dd):")
    dob_label.pack()
    dob_entry = tk.Entry(create_user_window)
    dob_entry.pack()

    role_label = tk.Label(create_user_window, text="Role:")
    role_label.pack()

    # Create a variable to hold the selected role
    role_var = tk.StringVar()
    role_var.set("Patient")  # Set an initial default role

    # Create a dropdown menu for selecting the role
    role_options = ["Patient", "Doctor"]
    role_dropdown = tk.OptionMenu(create_user_window, role_var, *role_options)
    role_dropdown.pack()

    # Create a label to display the selected role
    selected_role_label = tk.Label(create_user_window, text=f"Selected Role: {role_var.get()}")
    selected_role_label.pack()

    def on_role_change(*args):
        selected_role_label.config(text=f"Selected Role: {role_var.get()}")

    role_var.trace("w", on_role_change)  # Observe changes to role_var

    def submit_user():
        # Retrieve user input
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        password_confirm = password_confirm_entry.get()
        dob = dob_entry.get()
        role = role_var.get()

        # Check if any of the required fields are empty
        if not first_name or not last_name or not username or not email or not password or not dob:
            messagebox.showerror("Error", "Please fill in all the required fields.")
            return

        # Check if the username meets the length requirement
        if len(username) < 6:
            messagebox.showerror("Error", "Username must be at least 6 characters long.")
            return
        
        # Check if the user already exists in the database
        if user_exists(username, first_name, last_name):
            messagebox.showerror("Error", "User with the provided first name and last name already exists in the database. Please contact support if you think there's an error.")
            return

        # Check if the password meets the length requirement
        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return

        # Check if the password and password confirmation match
        if password != password_confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        # User details into the database
        db = mysql.connector.connect(
            host="69.23.75.181",
            user="CMAdmin",
            password="Chucky123",
            database="brain_cancer_mock_data"
        )
        cursor = db.cursor()

        # Generate the next available user ID
        cursor.execute("SELECT MAX(userId) FROM user")
        result = cursor.fetchone()
        next_user_id = 1 if result[0] is None else result[0] + 1

        # Hash the password
        hashed_pw = hashed_password(password)

        # Insert the new user into the database
        cursor.execute("INSERT INTO user (userId, firstName, lastName, username, email, password, dateOfBirth, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (next_user_id, first_name, last_name, username, email, hashed_pw, dob, role))
        db.commit()

        cursor.close()
        db.close()

        create_user_window.withdraw()  # Hide the create user window
        #login_window.deiconify()  # Show the login window
        messagebox.showinfo("User Created", "User created successfully.")

    # Create and pack a button to submit user details
    submit_button = tk.Button(create_user_window, text="Submit", command=submit_user)
    submit_button.pack()

    back_button = tk.Button(create_user_window, text="Back", command=create_user_window.destroy)
    back_button.place(relx=0, rely=0)

    create_user_window.mainloop()

def logout():
    main_window.destroy()  
    login_window.deiconify()  

def show_main_window():
    global main_window, welcome_label, user_role

    main_window = tk.Tk()
    main_window.title("Image Uploader")
    main_window.geometry("600x400")
    main_window.resizable(False, False) 
   

    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()

    window_width = 400
    window_height = 400

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    welcome_label = tk.Label(main_window, text="", font=("Arial", 12))
    welcome_label.pack(side="top", anchor="w")

    detector_label = tk.Label(main_window, text="Brain Cancer Detector", font=("Arial", 14))
    detector_label.pack(pady=10)

    message_frame = tk.Frame(main_window)
    message_frame.pack(side="bottom")

    validation_label = tk.Label(message_frame, text="", font=("Arial", 12))
    validation_label.pack()

    error_label = tk.Label(message_frame, text="", font=("Arial", 12), fg="red")
    error_label.pack()

    username = username_entry.get()

    db = mysql.connector.connect(
        host="69.23.75.181",
        user="CMAdmin",
        password="Chucky123",
        database="brain_cancer_mock_data"
    )
    cursor = db.cursor()

    cursor.execute("SELECT role FROM user WHERE username = %s", (username,))
    user_role = cursor.fetchone()

    cursor.close()
    db.close()

    if user_role:
        user_role = user_role[0]

        if user_role == "Doctor":
            show_doctor_main_window()
            welcome_label.config(text=f"Hi Dr {last_name}, {first_name}" if user_role == "Doctor" else f"Hi {first_name}, {last_name}")
        elif user_role == "Patient":
            show_patient_main_window()
            welcome_label.config(text=f"Hi {first_name}, {last_name}")
    else:
        messagebox.showerror("Role Error", "User role not found.")

    # Log Out button placed in the top-right corner
    logout_button = tk.Button(main_window, text="Log Out", command=logout)
    logout_button.place(relx=0.8, rely=0)

    main_window.mainloop()

def on_search_button_click():
    global search_entry, search_results_listbox
    search_term = search_entry.get()
    search_results_listbox.delete(0, tk.END)  
    search_patients_and_display(search_term)

def show_doctor_main_window():
    # Function for doctor-specific actions
    # You can place your code for scanning files and folders here
    welcome_label.config(text=f"Hi Dr {last_name}, {first_name}")

    folder_button = tk.Button(main_window, text="Scan Folder", command=lambda: open_folder(main_window))
    folder_button.pack(pady=10)

    file_button = tk.Button(main_window, text="Scan Single File", command=lambda: open_file(main_window))
    file_button.pack(pady=5)

    global progress_label
    progress_label = tk.Label(main_window, text="", font=("Arial", 12))
    progress_label.pack()

    # Create a frame to hold the search and add user elements only for doctors
    search_frame = tk.Frame(main_window)
    search_frame.pack(side="top", pady=10)

    # Make search_entry a global variable
    global search_entry
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left")

    search_button = tk.Button(search_frame, text="Search", command=on_search_button_click)
    search_button.pack(side="left")

    add_user_button = tk.Button(search_frame, text="Add User", command=add_user)
    add_user_button.pack(side="left", padx=10)  

    # Make search_results_listbox a global variable
    global search_results_listbox
    search_results_listbox = tk.Listbox(main_window)
    search_results_listbox.pack(side="top", padx=10)

    # Log Out button placed in the top-right corner
    logout_button = tk.Button(main_window, text="Log Out", command=logout)
    logout_button.place(relx=0.87, rely=0)

    main_window.mainloop()
   
def show_patient_main_window():
    # Function for patient-specific actions
    # Display a message for patients
    welcome_label.config(text=f"Hi {first_name}, {last_name}")

    message_label = tk.Label(main_window, text="No results at the moment. Please come back later.", font=("Arial", 12))
    message_label.pack()

    # Log Out button placed in the top-right corner
    logout_button = tk.Button(main_window, text="Log Out", command=logout)
    logout_button.place(relx=0.87, rely=0)

    main_window.mainloop()

def generate_activation_key():
    # Generate a random activation key (e.g., 12 characters)
    key_length = 12
    activation_key = ''.join(random.choices(string.ascii_letters + string.digits, k=key_length))
    return activation_key

def check_verification():
    key = None

    # Set up MySQL connection
    db = mysql.connector.connect(
        host="69.23.75.181",
        user="CMAdmin",
        password="Chucky123",
        database="brain_cancer_mock_data"
    )
    cursor = db.cursor()

    # Execute a SELECT query
    cursor.execute("SELECT activation FROM user WHERE username = %s AND activation = 0", (username_entry.get(),))

    result = cursor.fetchone()  # Fetch the first result

    verification_window = tk.Tk()
    verification_window.title("Verification")
    verification_window.geometry("400x400")
    verification_window.resizable(False, False) 

    if result:
        if result[0] == 0:
            key = generate_activation_key()
            send_activation_email(get_email(), key)

            verification_output = tk.Label(verification_window, text="You are not yet verified\nPlease enter the activation key sent to your email address:")
            verification_output.pack()
            verification_entry = tk.Entry(verification_window)
            verification_entry.pack()

            def resend_activation_email():
                diff_key = generate_activation_key()
                email = get_email()
                send_activation_email(email, diff_key)
                key = diff_key

            def verify_activation_key():
                nonlocal key  # Use nonlocal to indicate that we are modifying the outer variable
                activation_key = verification_entry.get()

                # Check if the activation key is valid
                if activation_key == key:
                    cursor.execute("UPDATE user SET activation = 1 WHERE username = %s", (username_entry.get(),))
                    db.commit()
                    messagebox.showinfo("Success!", "Account now activated.")
                    verification_window.destroy()
                else:
                    messagebox.showerror("Error", "Invalid activation key. Please try again.")

            retry_button = tk.Button(verification_window, text="Retry", command=resend_activation_email)
            retry_button.pack(pady=5)

            verify_button = tk.Button(verification_window, text="Verify", command=verify_activation_key)
            verify_button.pack(pady=5)
        else:
            verification_window.withdraw()
    else:
        cursor.execute("SELECT activation FROM user WHERE username = %s AND activation = 1", (username_entry.get(),))
        other_result = cursor.fetchone()
        if other_result[0] == 1:
            return
        else:
            error_output = tk.Label(verification_window, text="Error trying to fetch result...")
            error_output.pack()

    verification_window.mainloop()

def get_email():
    db = mysql.connector.connect(
        host="69.23.75.181",
        user="CMAdmin",
        password="Chucky123",
        database="brain_cancer_mock_data"
    )
    cursor = db.cursor()

    # Execute a SELECT query
    cursor.execute("SELECT email FROM user WHERE username = %s", (username_entry.get(),))

    result = cursor.fetchone()  # Fetch the first result

    if result:
        return str(result[0])
    else:
        messagebox.showerror("Error", "Email not found.")
    return None

def send_activation_email(email, activation_key):
    try:
        service = create_service()
        message = create_message(os.getenv('EMAIL'), email, 'Activation Key', f'Your activation key is: {activation_key}')
        message = (service.users().messages().send(userId="me", body=message).execute())
        # print("Message sent")
    except Exception as e:
        print(e)

def open_folder(root):
    check_verification()
    
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        jpg_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.dcm'))]
        total_images = len(jpg_files)

        if total_images == 0:
            progress_label.config(text="No .jpg images found in the selected folder", fg="red")
        else:
            choice = simpledialog.askstring("Select Option", "Enter 'custom' to enter a custom folder name or 'existing' to select an existing folder:")

            if choice:
                if choice.lower() == "custom":
                    custom_folder_name = simpledialog.askstring("Custom Folder Name", "Enter the name of the output folder:")

                    if custom_folder_name:
                        output_folder = filedialog.askdirectory(title="Select Output Folder")

                        if output_folder:
                            custom_output_folder = os.path.join(output_folder, custom_folder_name)
                            os.makedirs(custom_output_folder, exist_ok=True)

                            for i, file_name in enumerate(jpg_files, start=1):
                                file_path = os.path.join(folder_path, file_name)

                                if file_path.lower().endswith('.dcm'):
                                    jpg_filename = os.path.splitext(os.path.basename(file_name))[0] + '.jpg'
                                    jpg_output_path = os.path.join(custom_output_folder, jpg_filename)
                                    dcm_to_jpg(file_path, jpg_output_path)
                                else:
                                    output_path = os.path.join(custom_output_folder, os.path.basename(file_path))
                                    shutil.copy(file_path, output_path)

                                progress_label.config(text=f"Scanning {i}/{total_images} images", fg="green")
                                root.update_idletasks()

                            progress_label.config(text=f"All the images are successfully uploaded to the folder", fg="green")
                elif choice.lower() == "existing":
                    output_folder = filedialog.askdirectory(title="Select Existing Output Folder")

                    if output_folder:
                        for i, file_name in enumerate(jpg_files, start=1):
                            file_path = os.path.join(folder_path, file_name)

                            if file_path.lower().endswith('.dcm'):
                                jpg_filename = os.path.splitext(os.path.basename(file_path))[0] + '.jpg'
                                jpg_output_path = os.path.join(output_folder, jpg_filename)
                                dcm_to_jpg(file_path, jpg_output_path)
                            else:
                                output_path = os.path.join(output_folder, os.path.basename(file_path))
                                shutil.copy(file_path, output_path)

                            progress_label.config(text=f"Scanning {i}/{total_images} images", fg="green")
                            root.update_idletasks()

                        progress_label.config(text=f"All the images are successfully uploaded to the folder", fg="green")
                else:
                    progress_label.config(text="Invalid choice. Enter 'custom' or 'existing'.", fg="red")
            else:
                progress_label.config(text="Invalid choice. Enter 'custom' or 'existing'.", fg="red")

def open_file(root):
    check_verification()
    
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.dcm")])

    if file_path:
        choice = simpledialog.askstring("Output Folder", "Enter 'custom' to enter a custom folder name or 'existing' to select an existing folder:")

        if choice:
            if choice.lower() == "custom":
                custom_folder_name = simpledialog.askstring("Custom Folder Name", "Enter the name of the output folder:")

                if custom_folder_name:
                    output_folder = filedialog.askdirectory(title="Select Output Folder")

                    if output_folder:
                        custom_output_folder = os.path.join(output_folder, custom_folder_name)
                        os.makedirs(custom_output_folder, exist_ok=True)

                        if file_path.lower().endswith('.dcm'):
                            jpg_filename = os.path.splitext(os.path.basename(file_path))[0] + '.jpg'
                            jpg_output_path = os.path.join(custom_output_folder, jpg_filename)
                            dcm_to_jpg(file_path, jpg_output_path)
                        else:
                            output_path = os.path.join(custom_output_folder, os.path.basename(file_path))
                            shutil.copy(file_path, output_path)

                        progress_label.config(text="The image is successfully uploaded to the folder", fg="green")
            elif choice.lower() == "existing":
                output_folder = filedialog.askdirectory(title="Select Existing Output Folder")

                if output_folder:
                    if file_path.lower().endswith('.dcm'):
                        jpg_filename = os.path.splitext(os.path.basename(file_path))[0] + '.jpg'
                        jpg_output_path = os.path.join(output_folder, jpg_filename)
                        dcm_to_jpg(file_path, jpg_output_path)
                    else:
                        output_path = os.path.join(output_folder, os.path.basename(file_path))
                        shutil.copy(file_path, output_path)
                    progress_label.config(text="The image is successfully uploaded to the folder", fg="green")
            else:
                progress_label.config(text="Invalid choice. Enter 'custom' or 'existing'.", fg="red")
        else:
            progress_label.config(text="Invalid choice. Enter 'custom' or 'existing'.", fg="red")

# This function will be called when the "Add User" button is clicked
def add_user():
    create_user() 

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x400")
    login_window.resizable(False, False) 

    # Set the background image
    background_image_path = "CS458_Brain_Tumor_Detection\Background.png"
    set_background_image(login_window, background_image_path)



    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack(pady=10)
    login_button.pack()

    create_user_button = tk.Button(login_window, text="Create a User", command=create_user)
    create_user_button.pack(pady=10)
    create_user_button.pack()


    login_window.mainloop()