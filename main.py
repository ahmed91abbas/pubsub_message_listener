import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from google.cloud import pubsub_v1
from threading import Lock
import environs


class Pubsub_subscriber:

    def __init__(self):
        env = environs.Env()
        env.read_env()
        try:
            self.default_project_id = env("PROJECT_ID")
            self.default_subscription_name = env("SUBSCRIPTION_NAME")
        except environs.EnvValidationError:
            self.default_project_id = ""
            self.default_subscription_name = ""
        self.lock = Lock()
        self.list_items = []
        self.create_gui()
        self.start_gui()

    def pubsub_listener(self):
        try:
            project_id = self.project_id_entry.get()
            subscription_name = self.subscription_name_entry.get()

            subscriber = pubsub_v1.SubscriberClient()
            subscription_path = subscriber.subscription_path(
                project_id, subscription_name)

            # Check if path exists
            subscriber.get_subscription(subscription_path)

            def callback(message):
                self.add_to_listbox(self.pubsub_message_to_dict(message))
                message.ack()

            subscriber.subscribe(subscription_path, callback=callback)

            self.update_settings_frame_widgets()
            self.save_env_file(project_id, subscription_name)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pubsub_message_to_dict(self, message):
        attributes = message.attributes
        data = message.data
        publish_time = message.publish_time
        res = {}
        try:
            res["receive_time"] = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
            res["publish_time"] = publish_time.strftime("%Y-%m-%d, %H:%M:%S")
            res["attributes"] = dict(attributes)
            res["data"] = json.loads(data.decode("utf8"))
        except Exception as e:
            res["error"] = str(e)
        return res

    def update_settings_frame_widgets(self):
        self.project_id_entry.config(state='disabled')
        self.subscription_name_entry.config(state='disabled')
        self.connect_button.config(text='Connected',
                                   state='disabled',
                                   bg='#ccfa82')

    def create_gui(self):
        self.bg_color = '#e6e6ff'

        self.root = tk.Tk()
        self.root.title("Pubsub Subscriber")
        self.root.configure(background=self.bg_color)

        self.settings_frame = tk.Frame(self.root, bg=self.bg_color)
        self.info_frame = tk.Frame(self.root, bg=self.bg_color)
        self.body_frame = tk.Frame(self.root)
        self.settings_frame.pack(pady=10)
        self.info_frame.pack(pady=10)
        self.body_frame.pack(padx=15, pady=10)

        tk.Label(self.settings_frame,
                 text="Project ID:",
                 bg=self.bg_color).pack(side="left")
        self.project_id_entry = tk.Entry(self.settings_frame, width=40)
        self.project_id_entry.pack(side="left", padx=5)
        tk.Label(self.settings_frame,
                 text="Subscription name:",
                 bg=self.bg_color).pack(side="left", padx=5)
        self.subscription_name_entry = tk.Entry(self.settings_frame, width=40)
        self.subscription_name_entry.pack(side="left")
        self.project_id_entry.insert(0, self.default_project_id)
        self.subscription_name_entry.insert(0, self.default_subscription_name)
        self.connect_button = tk.Button(self.settings_frame,
                                        text="Connect",
                                        width=15,
                                        command=self.pubsub_listener)
        self.connect_button.pack(side="left", padx=20)

        self.count_label = tk.Label(self.info_frame,
                                    text="Count = 0",
                                    bg=self.bg_color,
                                    width=10)
        self.count_label.pack(side="left")
        tk.Button(self.info_frame,
                  text="Clear window",
                  width=20,
                  command=self.clear_listbox).pack(side="left", padx=20)

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

    def start_gui(self):
        self.root.mainloop()

    def mouse_click(self, event):
        widget = event.widget
        index = int(widget.curselection()[0])
        self.create_view_gui(self.list_items[index])

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

    def save_env_file(self, project_id, subscription_name):
        print("HERE")
        with open(".env", "w") as outf:
            outf.write(f"PROJECT_ID={project_id}\n")
            outf.write(f"SUBSCRIPTION_NAME={subscription_name}\n")


if __name__ == "__main__":
    Pubsub_subscriber()
