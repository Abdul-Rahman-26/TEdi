import tkinter as tk
import re

# Read the input text file
with open('./user_input.log' ,'r') as f:
    text = f.read()

# Tokenize the text into words
words = re.findall(r'\b[A-Za-z]+\b', text)

# Create a dictionary to store the frequency count of each word
freq_dict = {}
for i in range(len(words)-1):
    curr_word = words[i]
    next_word = words[i+1]
    if curr_word not in freq_dict:
        freq_dict[curr_word] = {}
    if next_word not in freq_dict[curr_word]:
        freq_dict[curr_word][next_word] = 0
    freq_dict[curr_word][next_word] += 1

# Find the most frequent next word for a given word
def most_frequent_next_word(word):
    if word in freq_dict:
        next_words = freq_dict[word]
        sorted_next_words = sorted(next_words.items(), key=lambda x: x[1], reverse=True)
        return sorted_next_words[0][0]
    else:
        return None

# Function to update last word variable
def update_last_word(event):
    text = event.widget.get("1.0", tk.END)
    words = re.findall(r'\b[A-Za-z]+\b', text)
    if words:
        last_word.set(words[-1])
        # Get the most frequent next word for the last word
        most_frequent = most_frequent_next_word(words[-1])
        # Update the suggestion box
        if most_frequent is not None:
            suggestion_box.configure(text=most_frequent)
    else:
        last_word.set("")

# Function to append suggestion to typed text
def append_suggestion(event):
    text = text_input.get("1.0", tk.END)
    suggestion = suggestion_box.cget("text")
    text_input.delete("1.0", tk.END)
    text_input.insert("1.0", text.strip() + " " + suggestion + " ")

# Create the main window
root = tk.Tk()

# Create a frame to hold the text input and suggestion box
input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP)

# Create a text input widget
text_input = tk.Text(input_frame, height=10, width=50)
text_input.pack(side=tk.LEFT)

# Create a label to show the suggestion
suggestion_box = tk.Label(input_frame, text="", font=("Arial", 12))
suggestion_box.pack(side=tk.BOTTOM, pady=10)

# Create a variable to hold the last word typed
last_word = tk.StringVar()
last_word.set("")

# Bind events to the text input widget
text_input.bind("<KeyRelease>", update_last_word)
text_input.bind("<KeyPress-4>", append_suggestion)

# Start the main loop
root.mainloop()
