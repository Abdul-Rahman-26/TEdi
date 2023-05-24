import tkinter as tk
from tensorflow.keras.models import load_model
import numpy as np
import pickle
# Importing Required libraries & Modules
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import random


# Create a Tkinter GUI
root = tk.Tk()

filename = None
title = StringVar()
status = StringVar()

# Load the model and tokenizer
model = load_model('next_words.h5')
tokenizer = pickle.load(open('token.pkl', 'rb'))

def predict_next_word(model, tokenizer, text):
    sequence = tokenizer.texts_to_sequences([text])
    if len(sequence[0]) > 0:
        sequence = np.array(sequence)
        preds = np.argmax(model.predict(sequence))
        predicted_word = ""
        for key, value in tokenizer.word_index.items():
            if value == preds:
                predicted_word = key
                break
        if predicted_word in tokenizer.word_index:
            return predicted_word
        else:
            random_words = set()
            while len(random_words) < 3:
                random_word = random.choice(list(tokenizer.word_index.keys()))
                random_words.add(random_word)
            return " ".join(random_words)
    else:
        random_words = set()
        while len(random_words) < 3:
            random_word = random.choice(list(tokenizer.word_index.keys()))
            random_words.add(random_word)
        return " ".join(random_words)


# Define a function to update the suggestion boxes based on user input
def update_suggestion_boxes(event=None):
    user_input = txtarea.get("1.0", "end-1c")
    if user_input:
        sequence = tokenizer.texts_to_sequences([user_input])[0]
        if len(sequence) > 2:
            last_words = sequence[-3:]
        else:
            last_words = sequence
        predicted_words = []
        while len(set(predicted_words)) < 3:
            predicted_word = predict_next_word(model, tokenizer, " ".join([tokenizer.index_word[idx] for idx in last_words]))
            last_words.append(tokenizer.word_index[predicted_word])
            predicted_words.append(predicted_word)
        for i, predicted_word in enumerate(predicted_words):
            suggestion_boxes[i].config(state="normal")
            suggestion_boxes[i].delete("1.0", tk.END)
            suggestion_boxes[i].insert(tk.END, predicted_word)
            suggestion_boxes[i].config(state="disabled")
    else:
        for i in range(3):
            suggestion_boxes[i].config(state="normal")
            suggestion_boxes[i].delete("1.0", tk.END)
            suggestion_boxes[i].insert(tk.END, predict_next_word(model, tokenizer, ""))
            suggestion_boxes[i].config(state="disabled")

# Define a function to insert the suggestion word into the user input box
def insert_suggestion_word(event=None):
    global typed_text
    user_input = txtarea.get("1.0", "end-1c")
    suggestion_word = ""
    if event.keysym_num == 49:
        suggestion_word = suggestion_boxes[0].get("1.0", "end-1c")
    elif event.keysym_num == 50:
        suggestion_word = suggestion_boxes[1].get("1.0", "end-1c")
    elif event.keysym_num == 51:
        suggestion_word = suggestion_boxes[2].get("1.0", "end-1c")
    if suggestion_word:
        if user_input:
            last_words = user_input.split()[-1:] # only get the last word
            user_input = " ".join( [suggestion_word])
        else:
            user_input = suggestion_word

        txtarea.insert(tk.END, user_input + " ") # add a space after the suggestion word
            # Call the update_suggestion_boxes function to update the suggestions based on the new user input
       

        update_suggestion_boxes()
        
    for i in range(3):
        suggestion_boxes[i].config(state="normal")
        suggestion_boxes[i].delete("1.0", tk.END)
        suggestion_boxes[i].config(state="disabled")


##############################################################################################################################################
# Creating Menubar
menubar = Menu(root, font=("times new roman", 15, "bold"), activebackground="skyblue")
root.config(menu=menubar)

# Creating File Menu
filemenu = Menu(menubar, font=("times new roman", 12, "bold"), activebackground="skyblue", tearoff=0)
# Adding New file Command
def newfile(*args):
    global filename
    ##########################################
    # Clearing the Text Area
    txtarea.delete("1.0",END)
    # Updating filename as None
    filename = None
    # Calling settitle funtion
    settitle()
    # updating status
    status.set("New File Created")
filemenu.add_command(label="New", font=("times new roman", 10), accelerator="Ctrl+N", command=newfile)

# Adding Open file Command

def openfile(*args):
    global filename
    # Exception handling
    try:
        # Asking for file to open
        filename = filedialog.askopenfilename(title="Select file",filetypes=(("All Files","*.*"),("Text Files","*.txt"),("Python Files","*.py"),("Pdf","*.pdf")))
        # checking if filename not none
        if filename:
            # opening file in readmode
            infile = open(filename,"r")
            # Clearing text area
            txtarea.delete("1.0",END)
            # Inserting data Line by line into text area
            for line in infile:
                txtarea.insert(END,line)
            # Closing the file  
            infile.close()
            # Calling Set title
            settitle()
            # Updating Status
            status.set("Opened Successfully")
    except Exception as e:
        messagebox.showerror("Exception",e)
filemenu.add_command(label="Open", font=("times new roman", 10), accelerator="Ctrl+O", command=openfile)

# Adding Save File Command
def savefile(*args):
    global filename
    # Exception handling
    try:
        # checking if filename not none
        if filename:
            # opening file in write mode
            outfile = open(filename,"w")
            # Writing data to file
            outfile.write(txtarea.get("1.0",END))
            # Closing the file
            outfile.close()
            # Calling settitle
            settitle()
            # Updating status
            status.set("Saved Successfully")
        else:
            # Calling SaveAs File Function
            saveasfile()
    except Exception as e:
        messagebox.showerror("Exception",e)
filemenu.add_command(label="Save", font=("times new roman", 10), accelerator="Ctrl+S", command=savefile)

# Defining Set Title Function
def settitle():
    global filename
    if filename:
        root.title(filename + " - Text Editor")
    else:
        root.title("Untitled - Text Editor")

# Defining Save As File Function
def saveasfile(*args):
    global filename
    # Exception handling
    try:
        # Asking for file name and type to save
        untitledfile = filedialog.asksaveasfilename(title="Save file As", defaultextension=".txt",
                                                    initialfile="Untitled.txt",
                                                    filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"),
                                                               ("Python Files", "*.py")))
        # Reading the data from text area
        data = txtarea.get("1.0", END)
        # Opening File in write mode
        outfile = open(untitledfile, "w")
        # Writing Data into file
        outfile.write(data)
        # Closing File
        outfile.close()
        # Updating filename as Untitled
        filename = untitledfile
        # Calling Set title
        settitle()
        # Updating Status
        status.set("Saved Successfully")
    except Exception as e:
        messagebox.showerror("Exception", e)

# Defining Exit Function
def exit(*args):
    op = messagebox.askyesno("WARNING", "Your Unsaved Data May be Lost!!")
    if op > 0:
        root.destroy()
    else:
        return

# Defining Cut Function
def cut(*args):
    txtarea.event_generate("<<Cut>>")

# Defining Copy Function
def copy(*args):
    txtarea.event_generate("<<Copy>>")

# Defining Paste Function
def paste(*args):
    txtarea.event_generate("<<Paste>>")

# Defining Undo Function
def undo(*args):
    global filename
    # Exception handling
    try:
        # checking if filename not none
        if filename:
            # Clearing Text Area
            txtarea.delete("1.0", END)
            # opening File in read mode
            infile = open(filename, "r")
            # Inserting data Line by line into text area
            for line in infile:
                txtarea.insert(END, line)
            # Closing File
            infile.close()
            # Calling Set title
            settitle()
            # Updating Status
            status.set("Undone Successfully")
        else:
            # Clearing Text Area
            txtarea.delete("1.0", END)
            # Updating filename as None
            filename = None
            # Calling Set title
            settitle()
            # Updating Status
            status.set("Undone Successfully")
    except Exception as e:
        messagebox.showerror("Exception", e)


# Creating Menu Bar
menubar = Menu(root)

# Creating File Menu
file = Menu(menubar, tearoff=0)
file.add_command(label="New")
file.add_command(label="Open")
file.add_command(label="Save", command=saveasfile)
file.add_command(label="Save As", command=saveasfile)
file.add_separator()
file.add_command(label="Exit", command=exit)


# Creating Menubar
menubar = Menu(root, font=("times new roman", 15, "bold"), activebackground="skyblue")
root.config(menu=menubar)

# Creating File Menu
filemenu = Menu(menubar, font=("times new roman", 12, "bold"), activebackground="skyblue", tearoff=0)
# Adding New file Command
filemenu.add_command(label="New", font=("times new roman", 10), accelerator="Ctrl+N", command=newfile)
# Adding Open file Command
filemenu.add_command(label="Open", font=("times new roman", 10), accelerator="Ctrl+O", command=openfile)
# Adding Save File Command
filemenu.add_command(label="Save", font=("times new roman", 10), accelerator="Ctrl+S", command=savefile)
# Adding Save As file Command
filemenu.add_command(label="Save As", font=("times new roman", 10), accelerator="Ctrl+Shift+s", command=saveasfile)
# Adding Seprator
filemenu.add_separator()
# Adding Exit window Command
filemenu.add_command(label="Exit", font=("times new roman", 10), accelerator="Ctrl+E", command=exit)
# Cascading filemenu to menubar
menubar.add_cascade(label="File", font=("times new roman", 10), menu=filemenu)

# Creating Edit Menu
editmenu = Menu(menubar, font=("times new roman", 12, "bold"), activebackground="skyblue", tearoff=0)
# Adding Cut text Command
editmenu.add_command(label="Cut", font=("times new roman", 10), accelerator="Ctrl+X", command=cut)
# Adding Copy text Command
editmenu.add_command(label="Copy", font=("times new roman", 10), accelerator="Ctrl+C", command=copy)
# Adding Paste text command
editmenu.add_command(label="Paste", font=("times new roman", 10), accelerator="Ctrl+V", command=paste)
# Adding Seprator
editmenu.add_separator()
# Adding Undo text Command
editmenu.add_command(label="Undo", font=("times new roman", 10), accelerator="Ctrl+U", command=undo)
# Cascading editmenu to menubar
menubar.add_cascade(label="Edit", font=("times new roman", 10), menu=editmenu)


################################################################################################################################################


root.geometry("1200x700+200+150") # Set the size of the window

root.title("TEdi")
#self.settitle()
icon = ImageTk.PhotoImage(Image.open('./Tedi.png'))
root.iconphoto(False, icon)


# Create a text input box
txtarea = tk.Text(root)
txtarea.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a variable to store the typed text
typed_text = ""


# Bind the keys "1", "2", and "3" to insert the corresponding suggestion word
bind_key_value = txtarea.bind("1", insert_suggestion_word)
bind_key_value = txtarea.bind("2", insert_suggestion_word)
bind_key_value = txtarea.bind("3", insert_suggestion_word)

# Bind the key "<KeyRelease>" to the update_suggestion_boxes function
bind_key_value =txtarea.bind("<space>", update_suggestion_boxes)

# Create suggestion boxes
suggestion_boxes = []
for i in range(3):
    suggestion_box = tk.Text(root, height=1, width=10, state="disabled", bg="white", fg="gray50")
    suggestion_box.pack(side=tk.LEFT, padx=5, pady=5)
    suggestion_boxes.append(suggestion_box)
    
def save_typed_text(event=None):
    user_input = txtarea.get("1.0", "end-1c")
    with open("typed_text.txt", "w") as f:
        f.write(user_input)

bind_key_value =txtarea.bind("<KeyRelease>", save_typed_text)

# Start the Tkinter event loop
root.mainloop()

