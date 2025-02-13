import inspect

from simprovhelper.base import send_experiment_executed_event

try:
    from tellurium.roadrunner import ExtendedRoadRunner
    from tellurium import getTelluriumVersion

except ImportError:
    raise ImportError("You need to install tellurium to use the tellurium helpers")
import pickle


def simulate_and_save_data(runner: ExtendedRoadRunner, data_file_path, **simulation_kwargs):
    def calling_file():
        # Get the current stack frame
        caller_frame = inspect.stack()[2]

        # Extract the file name from the caller's stack frame
        caller_file = caller_frame.filename

        return caller_file

    result = runner.simulate(**simulation_kwargs)
    pickle.dump(result, open(data_file_path, "wb"))
    send_experiment_executed_event(calling_file(), data_file_path, simulator_version=getTelluriumVersion(),
                                   simulator_formalism="Tellurium")
