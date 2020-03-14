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
        self.message_listener = Pubsub_message_listener(self, self.project_id, self.subscription_name)
        self.on_connect_button()
        self.root.mainloop()

    def create_gui(self):
        self.bg_color = '#e6e6ff'
        self.connected_color = '#ccfa82'
        self.disconnected_color = '#fc6f6f'
        font = ('calibri', 12, 'bold')

        self.root = tk.Toplevel()
        self.root.title("Pubsub Message Listener")
        self.root.configure(background=self.bg_color)
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)

        self.top_frame = tk.Frame(self.root, bg=self.bg_color)
        self.top_frame.pack(pady=10)
        self.info_frame = tk.Frame(self.root, bg=self.bg_color)
        self.info_frame.pack(pady=10)
        self.body_frame = tk.Frame(self.root)
        self.body_frame.pack(padx=15, pady=10)

        tk.Label(self.top_frame, text="Project ID", bg=self.bg_color).pack(padx=5, side="left")
        tk.Label(self.top_frame, text=self.project_id, borderwidth=2, relief="groove", width=35).pack(side="left")
        tk.Label(self.top_frame, bg=self.bg_color).pack(padx=5, side="left")
        tk.Label(self.top_frame, text="Subscription name", bg=self.bg_color).pack(padx=5, side="left")
        tk.Label(self.top_frame, text=self.subscription_name, borderwidth=2, relief="groove", width=35).pack(side="left")
        self.connect_button = tk.Button(self.top_frame, text="disconnected", bg=self.disconnected_color, width=15, command=self.on_connect_button)
        self.connect_button.pack(side="left", padx=20)

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

    def on_connect_button(self):
        if self.connect_button['text'] == 'disconnected':
            self.message_listener.connect()
            self.connect_button.config(text='Connected', bg=self.connected_color)
        else:
            self.message_listener.disconnect()
            self.connect_button.config(text='disconnected', bg=self.disconnected_color)

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

    def on_close(self):
        self.message_listener.disconnect()
        self.root.destroy()


if __name__ == "__main__":
    Message_list_gui("test-project-id", "test-pubsub-topic-subscription").run()
