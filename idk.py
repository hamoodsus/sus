import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageFilter
import time
import openai
import requests
from io import BytesIO


# Set your OpenAI API key here
openai.api_key = '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'

class ChatbotApp:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot App")

        # Set initial theme (light mode)
        self.dark_mode = False

        # Set background image from URL
        image_url = "https://i.ibb.co/RgMTv7F/R-1.jpg"  # Replace with your image URL
        original_image = self.load_image_from_url(image_url)

        # Resize the image to match the screen dimensions
        resized_image = original_image.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()))

        # Convert the resized image to PhotoImage
        self.background_image = ImageTk.PhotoImage(resized_image)

        # Create a canvas and pack it to fill the entire window
        self.canvas = tk.Canvas(master, width=self.master.winfo_screenwidth(), height=self.master.winfo_screenheight())
        self.canvas.pack()

        # Create the image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        # Create a transparent frame for the chat
        self.chat_frame = tk.Frame(self.master)  # Transparent background
        self.chat_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.chat_frame = tk.Frame(self.master)  # Transparent background
        self.chat_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Configure the transparency level for the entire window
        self.master.attributes('-alpha', 0.9)  # Set transparency level

        # Create scrolled text for chat history
        self.chat_history = tk.Text(
            self.chat_frame, wrap=tk.WORD, width=80, height=20, font=("Arial", 12), bd=0, bg="white", padx=10, pady=10
        )
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Create entry for user input
        self.user_input_entry = tk.Entry(self.chat_frame, width=50, font=("Arial", 12), bd=0, bg="white")
        self.user_input_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Create "Send" button
        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message, bd=0, bg="#0084FF", fg="white")
        self.send_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        # Create a button to toggle dark mode
        self.dark_mode_button = tk.Button(master, text="Dark Mode", command=self.toggle_dark_mode, bd=0, bg="#0084FF", fg="white")
        self.dark_mode_button.pack(side=tk.BOTTOM, pady=10)

        # Perform initial chat with OpenAI
        self.chat_with_openai("")

        # Maximize the window
        master.attributes('-fullscreen', True)

    # ... (rest of the methods remain unchanged)

    def load_image_from_url(self, url):
      try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        return img
      except requests.exceptions.RequestException as e:
        print(f"Error loading image from URL: {e}")
        return None
      except PIL.UnidentifiedImageError as e:  # Fix this line
        print(f"Error identifying image file: {e}")
        return None
    def send_message(self):
        user_input = self.user_input_entry.get()
        self.update_chat_history(f"You: {user_input}")
        self.chat_with_openai(user_input)
        self.user_input_entry.delete(0, tk.END)

    def chat_with_openai(self, user_input):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        chatbot_response = response['choices'][0]['message']['content']
        self.update_chat_history(f"Chatbot: {chatbot_response}")

    def update_chat_history(self, message):
        if message.startswith("Chatbot:"):
            self.typing_effect(message)
        else:
            self.chat_history.insert(tk.END, message + "\n")
            self.chat_history.yview(tk.END)


    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            # Set dark mode colors
            self.master.configure(bg="#1E1E1E")  # Dark background color
            self.user_input_entry.configure(bg="#333333", fg="white")  # Dark text color
            self.send_button.configure(bg="#333333", fg="white")  # Dark button color
            self.dark_mode_button.configure(bg="#333333", fg="white")  # Dark button color
        else:
            # Set light mode colors
            self.master.configure(bg="white")  # Light background color
            self.user_input_entry.configure(bg="white", fg="black")  # Light text color
            self.send_button.configure(bg="#0084FF", fg="white")  # Light button color
            self.dark_mode_button.configure(bg="#0084FF", fg="white")  # Light button color
    def typing_effect(self, message):
        self.message_to_type = message
        self.current_char_index = 0
        self.type_next_char()
    def type_next_char(self):
        if self.current_char_index < len(self.message_to_type):
            char = self.message_to_type[self.current_char_index]
            self.chat_history.insert(tk.END, char)
            self.chat_history.yview(tk.END)
            self.current_char_index += 1
            self.master.after(50, self.type_next_char)
    
    def chat_with_dalle(self, description):
        response = openai.Davinci.create(
            engine="davinci",
            prompt=description,
            max_tokens=100
        )
        dalle_response = response['choices'][0]['text'].strip()
        self.update_chat_history(f"DALL·E 2: {dalle_response}")
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()