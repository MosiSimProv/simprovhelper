import subprocess
import sys

SIMPROV_HOST = "localhost"
SIMPROV_PORT = 5000

from urllib import request
import json


def configure(host="localhost", port=5000):
    """ Configures the host and port for the SimProv provenance capturer.

    :param str host:
        The host address to connect to.
    :param int port:
        The port to connect to.
    """
    global SIMPROV_HOST
    global SIMPROV_PORT
    SIMPROV_HOST = host
    SIMPROV_PORT = port


def send_event(event_type:str, **kwargs):
    """ Sends an event to the SimProv provenance capturer.

    By default, the event will be sent to http://localhost:5000/capturer/process-event.
    The host and port can be configured via :func:`configure`.

    Note: `python_version` and `python_package` are automatically detected and added to the event information.

    :param str event_type:
        The type of event to send.
    :param kwargs:
        The arguments to pass to the event type.
    """
    url = f"http://{SIMPROV_HOST}:{SIMPROV_PORT}/capturer/process-event"
    req = request.Request(url, method="POST")
    req.add_header('Content-Type', 'application/json')

    event = kwargs
    event["type"] = event_type
    event["python_version"] = sys.version
    event["python_packages"] = _get_installed_packages()

    data = json.dumps(event)
    data = data.encode()
    try:
        r = request.urlopen(req, data=data)
        r.read()
    except Exception:
        raise RuntimeError(f"Failed to send event to Simprov at {url}")


def _get_installed_packages():
    p = subprocess.Popen('pip freeze --exclude-editable', shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    result = p.stdout.read().decode("utf-8")
    return result
