from itertools import count
from tkinter import *
import customtkinter as tk
import cv2
from PIL import Image, ImageTk
from customtkinter import CTkImage
import webview, subprocess, os
# Setting appearance and color theme
tk.set_appearance_mode("dark")  
tk.set_default_color_theme("dark-blue")

# Creating the main window
root = tk.CTk() 
root.geometry("400x650") 

# Creating a frame
frame = tk.CTkFrame(master=root, border_color="black", border_width=10, corner_radius=0)  
frame.pack(fill="both", expand=True) 

# Notch on top center
notch = tk.CTkButton(master=frame, text='PYphone', width=100, height=40, fg_color='black', state=DISABLED)  
notch.place(x=200-50, y=-5) 

# Initialize video capture
cap = cv2.VideoCapture(0)  
current_frame = None  
label_widget = None 
count = 0  

# Function to show the frame from the webcam

def show_frame():
    global current_frame, label_widget 
    if label_widget is None:
        label_widget = tk.CTkLabel(root, text="")
        label_widget.place(x=0, y=0, relwidth=1, relheight=1)

    def update_frame():
        global current_frame  
        ret, frame = cap.read()
        if ret:
            current_frame = frame  
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            photo = CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
            label_widget.image = photo  
            label_widget.configure(image=photo)
        root.after(20, update_frame)

    update_frame()

 

# Button commands
def screenshot():
    global current_frame, count  
    if current_frame is not None:
        img_dir = r"C:\Users\jayam\OneDrive\Desktop\SoarCS Final\Images" 
        os.makedirs(img_dir, exist_ok=True)  
        name = f"frame{count}.jpg"
        cv2.imwrite(os.path.join(img_dir, name), current_frame)
        count += 1
    else:
        print("No frame to save")

# Function to display images from a directory
def showImg():
    global row, col
    img_dir = r"C:\Users\jayam\OneDrive\Desktop\SoarCS Final\Images" 
    for img_file in os.listdir(img_dir):
        if img_file.endswith(".png"):
            img_path = os.path.join(img_dir, img_file)
            image = Image.open(img_path)
            image.thumbnail((175, 200))  
            img = ImageTk.PhotoImage(image)
            
            # Create a label for each image and add it to the gallery frame
            img_label = tk.CTkLabel(master=gallery_frame, image=img, text="")
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.grid(row=row, column=col, padx=15, pady=10)
            col += 1
            if col > 1: 
                col = 0
                row += 1
            
def Camera():
    show_frame() 

# Function to open the gallery (currently just a placeholder)
def gallery():
    global gallery_frame, row, col
    gallery_frame = tk.CTkFrame(master=root)
    gallery_frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    row = 0
    col = 0
    image_refs = []  # List to keep references to images to prevent garbage collection
    img_dir = r"C:\Users\jayam\OneDrive\Desktop\SoarCS Final\Images"

    for img_file in os.listdir(img_dir):
        if img_file.endswith(".jpg") or img_file.endswith(".png"): 
            img_path = os.path.join(img_dir, img_file)
            image = Image.open(img_path)
            image.thumbnail((175, 200))  
            img = ImageTk.PhotoImage(image)
            image_refs.append(img)  # Keep reference to image
            
            # Create a label for each image and add it to the gallery frame
            img_label = tk.CTkLabel(master=gallery_frame, image=img, text="")
            img_label.image = img  # Keep reference to avoid garbage collection
            img_label.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 1: 
                col = 0
                row += 1




# Function to open Google in a webview
def google():
    webview.create_window('Google', 'http://www.google.com')  # Create a webview window for Google
    webview.start()  # Start the webview event loop

# Function to open Snake game in a webview
def Snake():
    subprocess.Popen(['python', 'Snake.py'])

# Function placeholders for other games
def Pong():
    subprocess.Popen(['python', 'pong_game.py'])

def sort_visual():
    subprocess.Popen(['python', 'Sort_visual.py'])

# Application dictionary mapping IDs to functions
buttons = {}
application = {
    1: ("Camera", Camera),
    2: ("Browser", google),
    3: ("Gallery", gallery),
    4: ("Snake", Snake),
    5: ("sort_visual", sort_visual),
    6: ("Pong", Pong),
}

# Function to create home screen with buttons
def create_home_screen():
    count = 0  # Initialize counter for button labels
    for i in range(3):  # Create 3 rows of buttons
        for j in range(2):  # Create 2 columns of buttons
            app_id = i * 2 + j + 1  # Calculate button ID
            app_title, app_command = application.get(app_id, ("", lambda: None))  # Get title and command from dictionary
            buttons[f"App{count}"] = tk.CTkButton(master=frame, text=app_title, command=app_command, height=120, width=150, corner_radius=10)  # Create a button
            buttons[f"App{count}"].grid(row=i + 2, column=j, padx=25, pady=50)  # Place the button in the grid
            count += 1  # Increment counter

# Function to quit the current view and return to the home page
def quit_camera(event=None):
    global label_widget, gallery_frame
    if label_widget is not None:
        label_widget.destroy()  # Destroy the label widget if it exists
        label_widget = None
    if gallery_frame is not None:
        gallery_frame.destroy()
        gallery_frame = None

    for widget in root.winfo_children():  # Iterate over all widgets in the root window
        if isinstance(widget, tk.CTkButton):  # Check if the widget is a CTkButton
            widget.destroy()  # Destroy the button widget
    create_home_screen()  

    
# Binding the ESC key to quit the current view and return to home screen
root.bind("<Escape>", quit_camera)

# Create the home screen initially
create_home_screen()

# Start the main loop
root.mainloop()