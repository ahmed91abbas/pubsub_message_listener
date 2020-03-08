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
            f.write(json.dumps(data, indent=2))

    def init_history(self, path):
        data = {
            "project_ids": [],
            "subscriptions": [],
            "credentials_path": "",
            "emulator_host": "",
            "emulator_port": ""
        }
        self.save_json(path, data)
        return data

    def start_gui(self):
        self.root.mainloop()

    def create_gui(self):
        main_title_font = ('calibri', 20, 'bold')
        title_font = ('calibri', 12, 'bold')
        desc_font = ('calibri', 11)
        bg_color = '#e6e6ff'
        button_color = '#ffffe6'
        separator_color = '#e3bff2'
        padx = 10
        pady = 10

        self.root = tk.Tk()
        self.root.configure(background=bg_color)
        self.root.title("Pub/Sub Message Listener")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)

        entry_frame = tk.Frame(self.root, bg=bg_color)
        entry_frame.pack(padx=padx, pady=pady, fill='both')
        tk.Frame(height=10, bd=1, bg=separator_color, relief=tk.SUNKEN).pack(pady=pady, fill=tk.X)
        credentials_frame = tk.Frame(self.root, bg=bg_color)
        credentials_frame.pack(pady=pady, fill='both')
        tk.Frame(height=10, bd=1, bg=separator_color, relief=tk.SUNKEN).pack(pady=pady, fill=tk.X)
        emulator_frame = tk.Frame(self.root, bg=bg_color)
        emulator_frame.pack(pady=pady, fill='both')
        tk.Frame(height=10, bd=1, bg=separator_color, relief=tk.SUNKEN).pack(pady=pady, fill=tk.X)
        buttons_frame = tk.Frame(self.root, bg=bg_color)
        buttons_frame.pack(pady=pady*2)

        # entry_frame components
        entry_frame_head = tk.Frame(entry_frame, bg=bg_color)
        entry_frame_head.pack()
        entry_frame_body = tk.Frame(entry_frame, bg=bg_color)
        entry_frame_body.pack()

        tk.Label(entry_frame_head, text="Pub/Sub Message Listener", font=main_title_font, bg=bg_color).pack()

        desc = "Enter the project ID and Pub/Sub topic subscription name\n"\
               "that you want to listen to incoming messages from"
        tk.Label(entry_frame_head, text=desc, font=desc_font, bg=bg_color).pack(pady=pady, fill="both")

        tk.Label(entry_frame_body, text="Project ID", bg=bg_color).grid(row=0, column=0, padx=padx)

        project_id_var = tk.StringVar()
        self.project_id_entry = tk.Entry(entry_frame_body, textvariable=project_id_var, width=40)
        self.project_id_entry.grid(row=0, column=1)

        menubutton = tk.Menubutton(entry_frame_body, indicatoron=True, bg=bg_color)
        menu = tk.Menu(menubutton, tearoff=False)
        menubutton.configure(menu=menu)
        for elem in self.history["project_ids"]:
            menu.add_radiobutton(label=elem, variable=project_id_var, value=elem)
        menubutton.grid(row=0, column=2)

        tk.Label(entry_frame_body, text="Subscription name", bg=bg_color).grid(row=1, column=0, padx=padx)

        subscription_var = tk.StringVar()
        self.subscription_entry = tk.Entry(entry_frame_body, textvariable=subscription_var, width=40)
        self.subscription_entry.grid(row=1, column=1)

        menubutton = tk.Menubutton(entry_frame_body, indicatoron=True, bg=bg_color)
        menu = tk.Menu(menubutton, tearoff=False)
        menubutton.configure(menu=menu)
        for elem in self.history["subscriptions"]:
            menu.add_radiobutton(label=elem, variable=subscription_var, value=elem)
        menubutton.grid(row=1, column=2)

        # credentials_frame components
        credentials_frame_head = tk.Frame(credentials_frame, bg=bg_color)
        credentials_frame_head.pack()
        credentials_frame_body = tk.Frame(credentials_frame, bg=bg_color)
        credentials_frame_body.pack()

        tk.Label(credentials_frame_head, text="Google Application Credentials", font=title_font, bg=bg_color).pack()

        desc = 'Enter the path to your GCP credentials file and\n'\
               'press "Connect" in order to connect to the cloud'
        tk.Label(credentials_frame_head, text=desc, font=desc_font, bg=bg_color).pack(pady=pady, fill="both")

        def on_browse():
            filename = filedialog.askopenfilename()
            if filename != "":
                self.credentials_entry.delete(0, "end")
                self.credentials_entry.insert(0, filename)
        google_credentials = self.history["credentials_path"]
        if not google_credentials and os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            google_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        self.credentials_entry = tk.Entry(credentials_frame_body, width=50)
        self.credentials_entry.insert(0, google_credentials)
        self.credentials_entry.pack(side="left", padx=padx)
        tk.Button(credentials_frame_body, text="Browse", bg=button_color, command=on_browse).pack(side="left", padx=padx)

        # emulator_frame components
        emulator_frame_head = tk.Frame(emulator_frame, bg=bg_color)
        emulator_frame_head.pack()
        emulator_frame_body = tk.Frame(emulator_frame, bg=bg_color)
        emulator_frame_body.pack()

        tk.Label(emulator_frame_head, text="Pub/Sub Emulator", font=title_font, bg=bg_color).pack()

        desc = 'Fill the host and port of your Pub/Sub emulator and\n'\
               'press "Connect to emulator". (Credentials will be ignored)'
        tk.Label(emulator_frame_head, text=desc, font=desc_font, bg=bg_color).pack(pady=pady, fill="both")

        tk.Label(emulator_frame_body, text="Host", bg=bg_color).grid(row=0, column=0, padx=padx)

        self.host_entry = tk.Entry(emulator_frame_body, width=20)
        self.host_entry.insert(0, self.history["emulator_host"])
        self.host_entry.grid(row=0, column=1)

        tk.Label(emulator_frame_body, text="Port", bg=bg_color).grid(row=1, column=0, padx=padx)

        self.port_entry = tk.Entry(emulator_frame_body, width=20)
        self.port_entry.insert(0, self.history["emulator_port"])
        self.port_entry.grid(row=1, column=1, pady=3)

        # buttons_frame components
        button_width = 15
        button_height = 2
        tk.Button(buttons_frame, text="Connect", width=button_width, height=button_height, bg=button_color, command=self.on_connect).pack(side="left", padx=padx)
        tk.Button(buttons_frame, text="Connect to emulator", width=button_width, height=button_height, bg=button_color, command=self.on_emulator_connect).pack(side="left", padx=padx)
        tk.Button(buttons_frame, text="Exit", width=button_width, height=button_height, bg=button_color, command=self.on_close).pack(side="left", padx=padx)

    def on_connect(self):
        if not self.valid_pubsub_entries():
            return
        credentials_path = self.credentials_entry.get()
        if not credentials_path:
            messagebox.showerror("Error", "Couldn't find the Google credetials. Please add the bath to your Google credentials file.")
            return
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.save_current_entries()
        Message_list_gui(self.project_id_entry.get(), self.subscription_entry.get()).run()

    def on_emulator_connect(self):
        if not self.valid_pubsub_entries():
            return
        host = self.host_entry.get()
        port = self.port_entry.get()
        if not host or not port:
            messagebox.showerror("Error", "You must specifiy the host and port of the Pub/Sub emulator.")
            return
        os.environ["PUBSUB_EMULATOR_HOST"] = "{}:{}".format(host, port)
        self.save_current_entries()
        Message_list_gui(self.project_id_entry.get(), self.subscription_entry.get()).run()

    def valid_pubsub_entries(self):
        if not self.project_id_entry.get() or not self.subscription_entry.get():
            messagebox.showerror("Error", "You must specifiy the project ID and the subscription name.")
            return False
        return True

    def save_current_entries(self):
        if self.project_id_entry.get():
            self.history["project_ids"].append(self.project_id_entry.get())
            self.history["project_ids"] = list(set(self.history["project_ids"]))

        if self.subscription_entry.get():
            self.history["subscriptions"].append(self.subscription_entry.get())
            self.history["subscriptions"] = list(set(self.history["subscriptions"]))

        if self.credentials_entry:
            self.history["credentials_path"] = self.credentials_entry.get()

        if self.host_entry:
            self.history["emulator_host"] = self.host_entry.get()

        if self.port_entry:
            self.history["emulator_port"] = self.port_entry.get()

        self.save_json("history.json", self.history)

    def on_close(self):
        self.root.destroy()
        sys.exit(1)

if __name__ == "__main__":
    Main()
