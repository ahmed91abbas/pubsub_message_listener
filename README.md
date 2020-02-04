
# Pub/Sub message listener

By providing the Google Cloud project ID and a Pub/Sub topic subscription name you can listen to all incoming messages to that topic.

![main screen](https://github.com/ahmed91abbas/pubsub_message_listener/blob/master/images/main_gui.jpg?raw=true)

## Prerequisites

You need to have authentication setup with GCP with enough permissions to listen to the pub/sub topic you are trying to connect to. Please refer to the [GCP getting started with authentication article](https://cloud.google.com/docs/authentication/getting-started) to setup your authentication.

## Run the application

1. Create a new virtual environment running the following commands from the root of your project directory (Optional):

		virtualenv env

2. Activate your new virtual environment (Optional):
	- Linux:

			source env/bin/activate

	- Windows

			env\scripts\activate

3. Install all the Python packages needed for this application:

		pip install -r requirements.txt

4. Run the tool:

		python main.py
