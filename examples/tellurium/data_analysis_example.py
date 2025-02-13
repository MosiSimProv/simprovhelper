
###################
# This script is not meant to be executed.
###################

# Note: This is just an example how a general helper-function can be called.

import matplotlib.pyplot as plt
import pickle

from simprovhelper.base import send_data_analyzed_event

data_file = "./exp_results.pickle"
viz_file = "viz1.png"

data  = pickle.load(open(data_file, "rb"))
plt.plot(data[:, 0], data[:, 2] + data[:, 3])
plt.savefig(viz_file)
plt.show()
send_data_analyzed_event(data_file,visualization_path=viz_file,references=["R1.md","R2.md","R3.md"])