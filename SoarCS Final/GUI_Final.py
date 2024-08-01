from itertools import count
import subprocess
from tkinter import *
import customtkinter as tk
from PIL import Image, ImageTk
import os, webview, cv2


# Setting appearance and color theme
tk.set_appearance_mode("dark")  # Set the appearance mode to dark
tk.set_default_color_theme("dark-blue")  # Set the color theme

# Creating the main window
root = tk.CTk()  # Create the main window using CustomTkinter
root.geometry("400x650")  # Set the size of the main window

# Creating a frame
frame = tk.CTkFrame(master=root, border_color="black", border_width=10, corner_radius=0)  # Create a frame with a border
frame.pack(fill="both", expand=True)  # Pack the frame to fill the window

# Notch on top center
notch = tk.CTkButton(master=frame, text='PYphone', width=100, height=40, fg_color='black', state=DISABLED)  # Create a disabled button as a notch
notch.place(x=200-50, y=-5)  # Place the notch button at the top center

# Initialize video capture
cap = cv2.VideoCapture(0)  # Initialize video capture from the default camera
current_frame = None  # Global variable to store the current frame
label_widget = None  # Global variable for the video display label
count = 0  # Global counter for screenshots

# Function to show the frame from the webcam
def show_frame():
    global current_frame, label_widget  # Declare current_frame and label_widget as global

    if label_widget is None:
        label_widget = tk.CTkLabel(master=root)  # Create a label to display the video
        label_widget.place(x=0, y=0, relwidth=1, relheight=1)  # Place the label to fill the window

    def update_frame():
        global current_frame  # Declare current_frame as global
        ret, frame = cap.read()  # Read a frame from the webcam
        if ret:
            current_frame = frame  # Update current frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame to RGB
            img = Image.fromarray(frame)  # Convert frame to PIL image
            photo = tk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))  # Create a CTkImage from PIL image

            if label_widget:  # Ensure label_widget is not None
                label_widget.configure(image=photo, text = "")  # Configure the label to display the image
                label_widget.image = photo  # Store the image in the label to prevent garbage collection

        root.after(20, update_frame)  # Update the frame every 20 milliseconds

    update_frame()  # Start updating the frame

    # Create and place a button to save the current photo
    save_photo = tk.CTkButton(master=root, text="Save Photo", width=20, command=screenshot, height=20, border_width=0, corner_radius=30)
    save_photo.pack(side=BOTTOM)
    save_photo.place(x=200, y=500)


# Button command to save a screenshot
def screenshot():
    global current_frame, count  # Declare current_frame and count as global
    if current_frame is not None:
        os.chdir(r"C:\Users\jayam\OneDrive\Desktop\SoarCS Final\Images")  # Change directory to save the image
        name = f"frame{count}.jpg"  # Create a filename for the image
        cv2.imwrite(name, current_frame)  # Save the current frame as an image
        count += 1  # Increment the counter for the next screenshot
    else:
        print("No frame to save")  # Print a message if no frame is available

# Function to display images from a directory
def showImg():
    img_dir = r"C:\Users\jayam\OneDrive\Desktop\SoarCS Final\Images"  # Directory containing images
    for img in os.listdir(img_dir):  # List all files in the directory
        if img.endswith(".png"):  # Check if the file is a PNG image
            Label(root, image=PhotoImage(file=os.path.join(img_dir, img)))  # Create a label to display the image
            
# Function to open the camera view
def Camera():
    show_frame()  # Call the function to show the webcam feed

# Function to open the gallery (currently just a placeholder)
def gallery():
    global gallery_frame
    gallery_frame = tk.CTkFrame(master=root)
    gallery_frame.place(x=0, y=0, relwidth=1, relheight=1)

    img_dir = r"C:\Users\jayam\OneDrive\Desktop\SoarCS Final\Images"

    row = 0
    col = 0
    for img_file in os.listdir(img_dir):
        if img_file.endswith(".jpg") or img_file.endswith(".png"):
            img_path = os.path.join(img_dir, img_file)
            image = Image.open(img_path)
            image.thumbnail((200, 200))
            img = ImageTk.PhotoImage(image)

            # Create a label for each image and add it to the gallery frame
            img_label = tk.CTkLabel(master=gallery_frame, image=img, text="")
            img_label.image = img
            img_label.grid(row=row, column=col, padx=12, pady=10)
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
    5: ("Pong", Pong),
    6: ("Sort Visual", sort_visual),
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
def quit_app(event=None):
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
    

    create_home_screen()  # Recreate the home screen

# Binding the ESC key to quit the current view and return to home screen
root.bind("<Escape>", quit_app)

# Create the home screen initially
create_home_screen()

# Start the main loop
root.mainloop()
