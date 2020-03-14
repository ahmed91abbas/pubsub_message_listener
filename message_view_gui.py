import tkinter as tk
import json


class Message_view_gui:

    def __init__(self, json_data):
        self.create_view_gui(json_data)

    def create_view_gui(self, json_data):
        top = tk.Toplevel()
        top.title("View window")
        frame = tk.Frame(top)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side='right', fill=tk.Y)
        text_box = tk.Text(frame, width=100, height=60)
        text_box.pack()
        text_box.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_box.yview)
        frame.pack()

        text = json.dumps(json_data,
                          indent=2,
                          ensure_ascii=False).encode('utf8')
        text_box.insert(tk.END, text.decode())
