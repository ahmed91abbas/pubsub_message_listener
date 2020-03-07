import json
import sys
import os

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from message_list_gui import Message_list_gui


class Main:

    def __init__(self):
        history_file_path = "history.json"
        try:
            self.history = self.read_json(history_file_path)
        except FileNotFoundError:
            self.history = self.init_history(history_file_path)
        self.create_gui()
        self.start_gui()

    def read_json(self, path):
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)
    
    def save_json(self, path, data):
        with open(path, "w", encoding="utf8") as f:
            f.write(json.dumps(data))

    def init_history(self, path):
        data = {
            "project_ids": [],
            "subscriptions": []
        }
        self.save_json(path, data)
        return data

    def start_gui(self):
        self.root.mainloop()

    def create_gui(self):
        bg_color = '#e6e6ff'
        button_color = '#ffffe6'
        padx = 10
        pady = 5

        self.root = tk.Tk()
        self.root.configure(background=bg_color)
        self.root.title("Pub/Sub Message Listener")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)

        entry_frame = tk.Frame(self.root, bg=bg_color)
        entry_frame.pack()
        credentials_frame = tk.Frame(self.root, bg=bg_color)
        credentials_frame.pack()
        emulator_frame = tk.Frame(self.root, bg=bg_color)
        emulator_frame.pack()
        buttons_frame = tk.Frame(self.root, bg=bg_color)
        buttons_frame.pack()

        # entry_frame components
        tk.Label(entry_frame, text="Project ID", bg=bg_color).grid(row=0, column=0, padx=padx)

        project_id_var = tk.StringVar()
        self.project_id_entry = tk.Entry(entry_frame, textvariable=project_id_var, width=40, bg=bg_color)
        self.project_id_entry.grid(row=0, column=1)

        menubutton = tk.Menubutton(entry_frame, indicatoron=True, bg=bg_color)
        menu = tk.Menu(menubutton, tearoff=False)
        menubutton.configure(menu=menu)
        for elem in self.history["project_ids"]:
            menu.add_radiobutton(label=elem, variable=project_id_var, value=elem)
        menubutton.grid(row=0, column=2)

        tk.Label(entry_frame, text="Subscription name", bg=bg_color).grid(row=1, column=0, padx=padx)

        subscription_var = tk.StringVar()
        self.subscription_entry = tk.Entry(entry_frame, textvariable=subscription_var, width=40, bg=bg_color)
        self.subscription_entry.grid(row=1, column=1)

        menubutton = tk.Menubutton(entry_frame, indicatoron=True, bg=bg_color)
        menu = tk.Menu(menubutton, tearoff=False)
        menubutton.configure(menu=menu)
        for elem in self.history["subscriptions"]:
            menu.add_radiobutton(label=elem, variable=subscription_var, value=elem)
        menubutton.grid(row=1, column=2)

        # credentials_frame components
        def on_browse():
            filename = filedialog.askopenfilename()
            if filename != "":
                self.credentials_entry.delete(0, "end")
                self.credentials_entry.insert(0, filename)
        google_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        self.credentials_entry = tk.Entry(credentials_frame, text=google_credentials, width=50, bg=bg_color)
        self.credentials_entry.pack(side="left", padx=padx)
        tk.Button(credentials_frame, text="Browse", command=on_browse).pack(side="left", padx=padx)

        # emulator_frame components
        tk.Label(emulator_frame, text="Host", bg=bg_color).grid(row=0, column=0, padx=padx)

        self.host_entry = tk.Entry(emulator_frame, width=20, bg=bg_color)
        self.host_entry.grid(row=0, column=1)

        tk.Label(emulator_frame, text="Port", bg=bg_color).grid(row=1, column=0, padx=padx)

        self.port_entry = tk.Entry(emulator_frame, width=20, bg=bg_color)
        self.port_entry.grid(row=1, column=1)

        # buttons_frame components
        button_width = 17
        tk.Button(buttons_frame, text="Connect", width=button_width, command=self.on_connect).pack(side="left", padx=padx)
        tk.Button(buttons_frame, text="Connect to emulator", width=button_width, command=self.on_emulator_connect).pack(side="left", padx=padx)
        tk.Button(buttons_frame, text="Exit", width=button_width, command=self.on_close).pack(side="left", padx=padx)

    def on_connect(self):
        credentials_path = self.credentials_entry.get()
        if not credentials_path:
            messagebox.showerror("Error", "Couldn't find the Google credetials. Please add the bath to your Google credentials file.")
            return
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        Message_list_gui()
    
    def on_emulator_connect(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        if not host or not port:
            messagebox.showerror("Error", "You must specifiy the host and port of the Pub/Sub emulator.")
            return
        os.environ["PUBSUB_EMULATOR_HOST"] = "{}:{}".format(host, port)
        Message_list_gui()

    def on_close(self):
        self.root.destroy()
        sys.exit(1)

if __name__ == "__main__":
    Main()
