import tkinter as tk
import traceback
import sys
from tkinter import ttk
import subprocess


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200")
        self.title("Application")
        # Variables
        self.discord_token_var = tk.StringVar()
        self.channel_id_var = tk.StringVar()
        self.gpt_api_key_var = tk.StringVar()
        self.quiz_god_input_var = tk.StringVar()
        # Widgets
        self.button_keyboard = ttk.Button(self, text="Button", command=self.self_destruct)
        self.button_keyboard.pack()
        self.entry_discord_token = ttk.Entry(self, show="*", textvariable=self.discord_token_var)
        self.entry_discord_token.pack()
        self.entry_channel_id = ttk.Entry(self, textvariable=self.channel_id_var)
        self.entry_channel_id.pack()
        self.entry_gpt_api_key = ttk.Entry(self, show="*", textvariable=self.gpt_api_key_var)
        self.entry_gpt_api_key.pack()
        ttk.Label(self, text="quiz_god Keybind:").pack()
        self.entry_quiz_god_input = ttk.Entry(self, textvariable=self.quiz_god_input_var)
        self.entry_quiz_god_input.pack()

        try:
            self.discord_bot_process = subprocess.Popen([sys.executable, "discordBot.py"])
        except Exception as e:
            print("Failed to start discordBot.py", str(e))
            print(traceback.format_exc())

        try:
            self.quiz_god_process = subprocess.Popen([sys.executable, "quizGod.py"])
        except Exception as e:
            print("Failed to start quizGod.py", str(e))
            print(traceback.format_exc())

    def on_press(self, event=None):
        self.unbind(event.char)
        self.bind(self.quiz_god_input_var.get(), self.on_press)

    def self_destruct(self):
        if self.discord_bot_process.poll() is None:
            self.discord_bot_process.terminate()

        if self.quiz_god_process.poll() is None:
            self.quiz_god_process.terminate()

        self.destroy()


def main():
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.self_destruct)
    app.mainloop()


if __name__ == "__main__":
    main()