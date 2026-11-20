import os
import stat

from const import PlaybackStatus

SUPPORTED_EVENTS = {
    "stop": PlaybackStatus.STOPPED,
    "start": PlaybackStatus.PLAYING
}

try:
    event = os.environ['SENDSPIN_EVENT']
except KeyError:
    print(f"No SENDSPIN_EVENT environment variable set.")
    exit()

if event not in SUPPORTED_EVENTS:
    print(f"Received unsupported event: '{event}'.")
    exit()

# Fetch DBus version of event
dbus_event = SUPPORTED_EVENTS[event]
print(f"Received sendspin event: '{event}' -> '{dbus_event}'.")

fifo = "/var/run/sendspin-mpris-proxy"
if stat.S_ISFIFO(os.stat(fifo).st_mode) is False:
    print(f"{fifo} is not a named pipe.")
    exit(1)

with open(fifo, "a") as f:
    print(f"Playback Status: {dbus_event}", file=f)

exit()
