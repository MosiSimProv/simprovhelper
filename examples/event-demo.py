from simprovhelper import send_event

# Note: This is just a stupid example showing to use the send event function.

###################
# This script is not meant to be executed.
###################


my_event_data = {"file":"foo.py", "file_type":"python"}
send_event("Experiment executed",**my_event_data)