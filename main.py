import tkinter as tk
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=API_KEY)

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

class ChatWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat with Gemini AI")
        
        # Larger chat frame with margin
        self.chat_frame = tk.Frame(root, width=600, height=400, padx=10, pady=10)
        self.chat_frame.pack()
        
        # Larger text area with line spacing
        self.conversation_text = tk.Text(self.chat_frame, height=20, width=50, wrap=tk.WORD, spacing1=5, spacing2=2)
        self.conversation_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.conversation_text.yview)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        
        self.conversation_text.config(yscrollcommand=self.scrollbar.set)
        
        # Larger input frame with margin
        self.input_frame = tk.Frame(root, width=600, height=100, padx=10, pady=10)
        self.input_frame.pack()
        
        self.input_label = tk.Label(self.input_frame, text="You: ")
        self.input_label.pack(side=tk.LEFT)
        
        # Larger input entry
        self.input_entry = tk.Entry(self.input_frame, width=70)
        self.input_entry.pack(side=tk.LEFT)
        self.input_entry.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)
        
        self.convo = model.start_chat(history=[])

    def send_message(self, event=None):
        message = self.input_entry.get()
        if message.strip() == "":
            return
        self.input_entry.delete(0, tk.END)
        
        self.convo.send_message(message)
        response = self.convo.last.text
        
        # Insert user message on the left and AI response on the right
        self.conversation_text.insert(tk.END, f"You: {message}\n", "user_message")
        self.conversation_text.insert(tk.END, f"AI: {response}\n", "ai_response")
        self.conversation_text.insert(tk.END, "-"*30 + "\n")
        self.conversation_text.see(tk.END)

        # Apply tags for formatting
        self.conversation_text.tag_config("user_message", justify="right")
        self.conversation_text.tag_config("ai_response")

if __name__ == "__main__":
    root = tk.Tk()
    chat_window = ChatWindow(root)
    root.mainloop()
