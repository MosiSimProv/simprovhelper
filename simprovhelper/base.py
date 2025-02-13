import base64
import inspect
import sys
from pathlib import Path

from simprovhelper import send_event, _get_installed_packages


def send_experiment_executed_event(experiment_path=None, data_paths=None, **experiment_event_data):
    if experiment_path is None:
        experiment_path = inspect.stack()[1].filename
    if data_paths is None:
        paths = []
        path_contents = []
    else:
        if not isinstance(data_paths, list):
            data_paths = [data_paths]
        paths = [str(Path(path).resolve()) for path in data_paths]
        if len(data_paths) == 1:
            path_contents = {}
        else:
            path_contents = {path: open(path, "r").read() for path in paths}
    experiment_event_data = {**experiment_event_data, **{
        "experiment_path": str(Path(experiment_path).resolve()),
        "data_paths": paths,
        "path_contents": path_contents}}
    send_event("Executing Simulation Experiment", **experiment_event_data)


def send_data_analyzed_event(used_simulation_data_paths, script_path=None, used_analysis_result_paths=None,
                             visualization_path: str = None,
                             analysis_result_path: str = None, references: [str] = None):
    if script_path is None:
        script_path = inspect.stack()[1].filename
    # Handle Datapaths
    if used_simulation_data_paths is None:
        raise RuntimeError("The used data_paths cannot be none.")
    if used_simulation_data_paths == "" or used_simulation_data_paths == []:
        raise RuntimeError("The used data_paths cannot be empty (meaning \"\" or [].")
    if not isinstance(used_simulation_data_paths, list):
        used_simulation_data_paths = [used_simulation_data_paths]
    paths = [str(Path(path).resolve()) for path in used_simulation_data_paths]

    analyzing_event_data = {
        "script_path": str(Path(script_path).resolve()),
        "script_content": open(script_path, "r").read(),
        "python_version": sys.version,
        "python_packages": _get_installed_packages(),
        "simulation_data_paths": paths}

    if references:
        analyzing_event_data["references"] = references

    if analysis_result_path:
        analysis_result_path = Path(analysis_result_path).resolve()
        if not analysis_result_path.exists():
            raise RuntimeError(
                f"Can't find analysis result at path {analysis_result_path}")
        analysis_result_content = open(analysis_result_path, "r").read()
        analyzing_event_data["analysis_result_path"] = str(analysis_result_path)
        analyzing_event_data["analysis_result_content"] = analysis_result_content

    if used_analysis_result_paths:
        for path in used_analysis_result_paths:
            used_analysis_result_path = Path(path).resolve()
            if not used_analysis_result_path.exists():
                raise RuntimeError(
                    f"Can't find used analysis result path {used_analysis_result_path}")
        analyzing_event_data["used_analysis_result_paths"] = used_analysis_result_paths

    if visualization_path:
        visualization_path = Path(visualization_path).resolve()
        if not visualization_path.exists():
            raise RuntimeError(
                f"Can't find used visualization at path {visualization_path}")
        visualization_content = None
        with open(visualization_path, "rb") as img_file:
            visualization_content = base64.b64encode(
                img_file.read()).decode("utf8")
        analyzing_event_data["visualization_path"] = str(visualization_path)
        analyzing_event_data["visualization_content"] = visualization_content

    send_event("Analyzing Simulation Data", **analyzing_event_data)
