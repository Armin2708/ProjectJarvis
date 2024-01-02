import json
import tkinter as tk
from tkinter import filedialog, messagebox

root = tk.Tk()
root.title("QuizGod Gui")
root.geometry("300x250")


def save_data():
    data = {
        'TesseractPath': TesseractPath,
        'OpenAiApiKey': OpenAiApiKey,
        'DiscordBotToken': DiscordBotToken,
        'DiscordChannel': DiscordChannel,
        'topLeftPosKey': topLeftPosKey,
        'botRightPosKey': botRightPosKey,
        'quizGodRunKey': quizGodRunKey,
        'autoDestructKey': autoDestructKey
    }

    with open('data.json', 'w') as f:
        json.dump(data, f)


def load_data():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


data = load_data()
TesseractPath = data.get('TesseractPath', [])
OpenAiApiKey = data.get('OpenAiApiKey', [])
DiscordBotToken = data.get('DiscordBotToken', [])
DiscordChannel = data.get('DiscordChannel', [])

topLeftPosKey = data.get('topLeftPosKey', [])
botRightPosKey = data.get('botRightPosKey', [])
quizGodRunKey = data.get('quizGodRunKey', [])
autoDestructKey = data.get('autoDestructKey', [])


def load_data():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def print_values():
    print("TesseractPath:", TesseractPath)
    print("OpenAiApiKey:", OpenAiApiKey)
    print("DiscordBotToken:", DiscordBotToken)
    print("DiscordChannel:", DiscordChannel)
    print("topLeftPosKey:", topLeftPosKey)
    print("botRightPosKey:", botRightPosKey)
    print("quizGodRunKey:", quizGodRunKey)
    print("autoDestructKey:", autoDestructKey)


def open_input_dialog(variable):

    def validate():
        txt = entry.get()
        variable.append(txt)
        messagebox.showinfo("String info", f"String saved: {txt}")
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Enter your string")
    entry = tk.Entry(top)
    entry.pack()

    submit_button = tk.Button(top, text="Validate", command=validate)
    submit_button.pack()


def open_path_dialog():
    global TesseractPath
    filepath = filedialog.askopenfilename()
    TesseractPath.append(filepath)
    messagebox.showinfo("Path Info", f"Path saved: {filepath}")


def open_key_dialog(variable):

    def validate():
        keys = entry.get()
        variable.append(keys.split(","))
        messagebox.showinfo("Key Combination", f"Key Combination saved: {keys}")
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Enter Key Combination")
    label = tk.Label(top, text="Enter keys separated by comma")
    label.pack()
    entry = tk.Entry(top)
    entry.pack()

    submit_button = tk.Button(top, text="Validate", command=validate)
    submit_button.pack()


func_button = tk.Button(root, text=f"Select Tesseract path", command=open_path_dialog)
func_button.pack()

key_button = tk.Button(root, text=f"Enter Api Key", command=lambda: open_input_dialog(OpenAiApiKey))
key_button.pack()
key_button = tk.Button(root, text=f"Enter DiscordBot Token", command=lambda: open_input_dialog(DiscordBotToken))
key_button.pack()
key_button = tk.Button(root, text=f"Enter Discord Channel", command=lambda: open_input_dialog(DiscordChannel))
key_button.pack()

func_button = tk.Button(root, text=f"Set Top left pos Key", command=lambda: open_key_dialog(topLeftPosKey))
func_button.pack()
func_button = tk.Button(root, text=f"Set Bot right pos Key", command=lambda: open_key_dialog(botRightPosKey))
func_button.pack()
func_button = tk.Button(root, text=f"Set Run Key", command=lambda: open_key_dialog(quizGodRunKey))
func_button.pack()
func_button = tk.Button(root, text=f"Set self Destruct Key", command=lambda: open_key_dialog(autoDestructKey))
func_button.pack()

print_button = tk.Button(root, text="Print values", command=print_values)
print_button.pack()

root.protocol("WM_DELETE_WINDOW", save_data)

root.mainloop()