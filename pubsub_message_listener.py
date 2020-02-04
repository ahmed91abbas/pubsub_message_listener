from google.cloud import pubsub_v1
from datetime import datetime
import json


class Pubsub_message_listener:

    def __init__(self, gui, project_id, subscription_name):
        self.gui = gui
        self.project_id = project_id
        self.subscription_name = subscription_name
        self.pubsub_listener()

    def pubsub_listener(self):
        try:
            subscriber = pubsub_v1.SubscriberClient()
            subscription_path = subscriber.subscription_path(
                self.project_id, self.subscription_name)

            # Check if path exists
            subscriber.get_subscription(subscription_path)

            def callback(message):
                self.gui.add_to_listbox(self.pubsub_message_to_dict(message))
                message.ack()

            subscriber.subscribe(subscription_path, callback=callback)

            self.gui.update_settings_frame_widgets()
            self.gui.save_env_file(self.project_id, self.subscription_name)
        except Exception as e:
            self.gui.show_error(str(e))

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