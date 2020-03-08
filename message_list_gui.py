import tkinter as tk
from tkinter import messagebox
import json
from threading import Lock
from pubsub_message_listener import Pubsub_message_listener
from message_view_gui import Message_view_gui


class Message_list_gui:

    def __init__(self, project_id, subscription_name):
        self.project_id = project_id
        self.subscription_name = subscription_name
        self.lock = Lock()
        self.list_items = []

    def run(self):
        self.create_gui()
        Pubsub_message_listener(self, self.project_id, self.subscription_name)
        self.root.mainloop()

    def create_gui(self):
        self.bg_color = '#e6e6ff'

        self.root = tk.Tk()
        self.root.title("Pubsub Message Listener")
        self.root.configure(background=self.bg_color)

        self.info_frame = tk.Frame(self.root, bg=self.bg_color)
        self.info_frame.pack(pady=10)
        self.body_frame = tk.Frame(self.root)
        self.body_frame.pack(padx=15, pady=10)

        tk.Label(self.info_frame, text="Project ID:", bg=self.bg_color).pack(side="left")
        tk.Label(self.info_frame, text=self.project_id, bg='#ccfa82').pack(side="left")
        tk.Label(self.info_frame, text="Subscription name:", bg=self.bg_color).pack(side="left")
        tk.Label(self.info_frame, text=self.subscription_name, bg='#ccfa82').pack(side="left")
        self.count_label = tk.Label(self.info_frame, text="Count = 0", bg=self.bg_color, width=10)
        self.count_label.pack(side="left")
        tk.Button(self.info_frame, text="Clear window", width=15, command=self.clear_listbox).pack(side="left", padx=20)

        scrollbar = tk.Scrollbar(self.body_frame)
        scrollbar.pack(side='right', fill=tk.Y)
        self.listbox = tk.Listbox(self.body_frame, width=200, height=40)
        self.listbox.pack()
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind('<Double-Button-1>', self.mouse_click)
        self.listbox.bind('<Return>', self.mouse_click)
        scrollbar.config(command=self.listbox.yview)

    def add_to_listbox(self, json_data):
        self.lock.acquire()

        self.list_items.append(json_data)
        self.count_label["text"] = f"Count = {len(self.list_items)}"
        text = json.dumps(json_data, ensure_ascii=False).encode('utf8')

        self.listbox.insert(tk.END, text.decode())
        if len(self.list_items) % 2 == 0:
            self.listbox.itemconfigure(tk.END, background='#f0f0ff')

        self.lock.release()

    def clear_listbox(self):
        self.list_items = []
        self.count_label["text"] = f"Count = {len(self.list_items)}"
        self.listbox.delete(0, tk.END)

    def mouse_click(self, event):
        widget = event.widget
        index = int(widget.curselection()[0])
        Message_view_gui(self.list_items[index])

    def show_error(self, message):
        messagebox.showerror("Error", message)


if __name__ == "__main__":
    Message_list_gui("csdf-dsadas", "dasd-dsadsa-dasd-das").run()
