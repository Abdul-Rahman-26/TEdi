import tkinter as tk
from tensorflow.keras.models import load_model
import numpy as np
import pickle

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
        return predicted_word
    else:
        return ""

# Define a function to update the suggestion boxes based on user input
def update_suggestion_boxes(event=None):
    user_input = input_box.get("1.0", "end-1c")
    if user_input:
        last_words = user_input.split()[-3:]
        for i in range(3):
            predicted_word = predict_next_word(model, tokenizer, " ".join(last_words))
            last_words.append(predicted_word)
            suggestion_boxes[i].config(state="normal")
            suggestion_boxes[i].delete("1.0", tk.END)
            suggestion_boxes[i].insert(tk.END, predicted_word)
            suggestion_boxes[i].config(state="disabled")
            if i == 2:
                break
    else:
        for i in range(3):
            suggestion_boxes[i].config(state="normal")
            suggestion_boxes[i].delete("1.0", tk.END)
            suggestion_boxes[i].config(state="disabled")


# Define a function to insert the suggestion word into the user input box
def insert_suggestion_word(event=None):
    user_input = input_box.get("1.0", "end-1c")
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
            user_input = " ".join(user_input.split()[-1:] + [suggestion_word])
        else:
            user_input = suggestion_word
        input_box.delete("1.0", tk.END)
        input_box.insert(tk.END, user_input + " ") # add a space after the suggestion word
        for i in range(3):
            suggestion_boxes[i].config(state="normal")
            suggestion_boxes[i].delete("1.0", tk.END)
            suggestion_boxes[i].config(state="disabled")

# Create a Tkinter GUI
root = tk.Tk()
root.title("Next Word Predictor")

# Create a text input box
input_box = tk.Text(root, height=5, width=50)
input_box.pack(side=tk.TOP, padx=10, pady=10)


# Bind the keys "1", "2", and "3" to insert the corresponding suggestion word
bind_key_value = input_box.bind("1", insert_suggestion_word)
bind_key_value = input_box.bind("2", insert_suggestion_word)
bind_key_value = input_box.bind("3", insert_suggestion_word)

# Bind the key "<KeyRelease>" to the update_suggestion_boxes function
bind_key_value =input_box.bind("<space>", update_suggestion_boxes)

# Create suggestion boxes
suggestion_boxes = []
for i in range(3):
    suggestion_box = tk.Text(root, height=1, width=10, state="disabled", bg="white", fg="gray50")
    suggestion_box.pack(side=tk.LEFT, padx=5, pady=5)
    suggestion_boxes.append(suggestion_box)

# Start the Tkinter event loop
root.mainloop()
