import customtkinter as ctk
from tkinter import messagebox
from tkinter import font
from Query import send_query
from Query import get_models
from tkinter import filedialog

# Color palette from the mockup
COLOR_BLACK = "#1B1C22"
COLOR_DARK_GREY = "#2D3036"
COLOR_LIGHT_GREY = "#3A3E49"
COLOR_DARK_WHITE = "#A5ADB6"
COLOR_OFF_WHITE = "#F4F5F6"
COLOR_RED = "#D24235"

# Set message limit
input_limit = 500

# Set the default model to use
MODEL = get_models()[0]

# Initialize main application window
app = ctk.CTk()
app.geometry("700x700")
app.minsize(700, 700)
app.title("FlashForge")
app.configure(fg_color=COLOR_BLACK)

# Load custom font
font_reg = ctk.CTkFont(
    family="Space Grotesk", 
    weight="normal", 
    size=16
)
font_bold = ctk.CTkFont(
    family="Space Grotesk", 
    weight="bold", 
    size=16
)

# Dropdown menu for selecting the model
model_var = ctk.StringVar(value=MODEL)

def update_model(*args):
    global MODEL
    MODEL = model_var.get()

model_var.trace("w", update_model)
model_dropdown_frame = ctk.CTkFrame(
    app,
    width=600,
    height=30,
    fg_color="transparent"
)
model_dropdown_frame.pack(pady=(25, 0))
model_dropdown = ctk.CTkOptionMenu(
    model_dropdown_frame,
    width=80,
    height=30,
    corner_radius=10,
    hover=False,
    dynamic_resizing=True,
    fg_color=COLOR_BLACK,
    text_color=COLOR_OFF_WHITE,
    button_color=COLOR_BLACK,
    button_hover_color=COLOR_DARK_GREY,
    dropdown_text_color=COLOR_OFF_WHITE,
    dropdown_fg_color=COLOR_BLACK,
    dropdown_hover_color=COLOR_DARK_GREY,
    font=font_reg,
    variable=model_var,
    values=get_models()
)
model_dropdown.pack()

# Chatbox window (output display)
chatbox = ctk.CTkTextbox(
    app, 
    width=700, 
    corner_radius=25, 
    wrap="word", 
    font=font_reg, 
    text_color=COLOR_OFF_WHITE, 
    fg_color="transparent"
)
chatbox.pack(
    fill="y", 
    expand=True
)
chatbox.configure(state="disabled")

# Divider between chatbox and user input
divider = ctk.CTkFrame(
    app, 
    width=600, 
    height=2, 
    fg_color=COLOR_DARK_GREY
)
divider.pack(
    side="top", 
)

# Frame to contain the divider
bottom_frame = ctk.CTkFrame(
    app, 
    width=600, 
    height=60, 
    corner_radius=0, 
    fg_color="transparent"
)
bottom_frame.pack()

# Create a frame inside bottom_frame
frame_center = ctk.CTkFrame(
    bottom_frame, 
    width=600, 
    height=60, 
    fg_color="transparent"
)
frame_center.pack(expand=True)

# Copy button
copy_button = ctk.CTkButton(
    frame_center, 
    width=80, 
    height=30, 
    corner_radius=10, 
    fg_color=COLOR_OFF_WHITE, 
    hover_color=COLOR_DARK_WHITE,
    text="Copy", 
    font=font_bold, 
    text_color=COLOR_BLACK
)
copy_button.pack(side="left", pady=15)

# Save button
save_button = ctk.CTkButton(
    frame_center, 
    width=80, 
    height=30, 
    corner_radius=10, 
    fg_color=COLOR_OFF_WHITE, 
    hover_color=COLOR_DARK_WHITE,
    text="Save", 
    font=font_bold, 
    text_color=COLOR_BLACK
)
save_button.pack(side="left", padx=(15, 15), pady=15)

# Load button
load_button = ctk.CTkButton(
    frame_center, 
    width=80, 
    height=30, 
    corner_radius=10, 
    fg_color=COLOR_OFF_WHITE, 
    hover_color=COLOR_DARK_WHITE,
    text="Load", 
    font=font_bold, 
    text_color=COLOR_BLACK
)
load_button.pack(side="left", padx=(0, 15), pady=15)

# Clear button
clear_button = ctk.CTkButton(
    frame_center, 
    width=80, 
    height=30, 
    corner_radius=10, 
    fg_color=COLOR_OFF_WHITE, 
    hover_color=COLOR_DARK_WHITE,
    text="Clear", 
    font=font_bold, 
    text_color=COLOR_BLACK
)
clear_button.pack(side="left", pady=15)

# User input textbox (for entering messages)
user_input_frame = ctk.CTkFrame(
    app, 
    width=650, 
    corner_radius=25, 
    fg_color=COLOR_DARK_GREY
)
user_input_frame.pack()
user_input = ctk.CTkTextbox(
    user_input_frame, 
    width=530, 
    height=150, 
    corner_radius=25, 
    fg_color="transparent", 
    wrap="word", 
    font=font_reg, 
    text_color=COLOR_OFF_WHITE
)
user_input.grid(
    row=0, 
    column=0, 
    padx=25, 
    pady=0, 
    sticky="nwse" 
)
user_input_frame.columnconfigure(
    0, 
    weight=1
)

# Send button (arrow icon)
send_button = ctk.CTkButton(
    user_input_frame, 
    width=40, 
    height=40, 
    corner_radius=10, 
    fg_color=COLOR_OFF_WHITE, 
    hover_color=COLOR_DARK_WHITE,
    text="⮝", 
    font=font_bold, 
    text_color=COLOR_BLACK
)
send_button.grid(
    row=0, 
    column=1, 
    padx=(15, 15), 
    pady=(15, 0), 
    sticky="ne"
)
send_button.columnconfigure(
    1, 
    weight=0
)

# Frame to contain the character limit indicator
char_limit_frame = ctk.CTkFrame(
    app, 
    width=600, 
    height=22.5, 
    fg_color="transparent"
)
char_limit_frame.pack(pady=(0, 2.5))

# Add character limit indicator inside the new frame
char_limit_label = ctk.CTkLabel(
    char_limit_frame, 
    width=100, 
    text=f"0 / {input_limit}", 
    font=font_reg, 
    text_color=COLOR_BLACK, 
    bg_color="transparent", 
    anchor="center"
)
char_limit_label.pack(expand=True)

# Function to copy chatbox content to clipboard
def copy_chatbox():
    app.clipboard_clear()
    app.clipboard_append(chatbox.get("1.0", "end").strip())

# Function to clear chatbox content
def clear_chatbox():
    chatbox.configure(state="normal")
    chatbox.delete("1.0", "end")
    chatbox.configure(state="disabled")

# Function to save chatbox content to a file
def save_chatbox():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(chatbox.get("1.0", "end").strip())

# Function to load chatbox content from a file
def load_chatbox():
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            chatbox.configure(state="normal")
            chatbox.delete("1.0", "end")
            chatbox.insert("1.0", content)
            chatbox.configure(state="disabled")

load_button.configure(command=load_chatbox)
save_button.configure(command=save_chatbox)
copy_button.configure(command=copy_chatbox)
clear_button.configure(command=clear_chatbox)

# Function to update character limit indicator
def update_char_limit(event):
    current_length = len(user_input.get("1.0", "end").strip())
    percentage = current_length / input_limit

    # Calculate the new color based on the percentage
    start_rgb = app.winfo_rgb(COLOR_BLACK)
    end_rgb = app.winfo_rgb(COLOR_OFF_WHITE)
    new_rgb = tuple(int(start + (end - start) * percentage) for start, end in zip(start_rgb, end_rgb))
    new_color = "#%04x%04x%04x" % new_rgb

    if current_length > input_limit:
        char_limit_label.configure(
            text=f"{current_length} / {input_limit}", 
            text_color=COLOR_RED
        )

    else:
        char_limit_label.configure(
            text=f"{current_length} / {input_limit}", 
            text_color=new_color
        )

# Bind the update_char_limit function to the user input textbox
user_input.bind(
    "<KeyRelease>", 
    update_char_limit
)

# Function to handle sending a message
def send_message():
    message = user_input.get("1.0", "end").strip()
    
    if len(message) > 0:
        if len(message) <= input_limit:
            user_input.delete(
                "1.0", 
                "end"
            )
            char_limit_label.configure(
                text=f"0 / {input_limit}", 
                text_color=COLOR_BLACK
            )
            # Query the AI model and display the response
            response = send_query(message, MODEL)
            chatbox.configure(
                state="normal"
            )
            chatbox.insert(
                "end", 
                f"{response}\n"
            )
            chatbox.configure(
                state="disabled"
            )
        else:
            messagebox.showwarning(
                "Warning", 
                f"Message exceeds {input_limit} character limit."
            )
    else:
        messagebox.showwarning(
            "Warning", 
            "Message cannot be empty."
        )

send_button.configure(
    command=send_message
)

app.mainloop()