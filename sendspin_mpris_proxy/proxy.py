import asyncio
import logging
import os
import re
import stat

from dbus_fast import BusType
from dbus_fast.aio import MessageBus

from .mpris import MediaPlayer2Interface, MediaPlayer2PlayerInterface

_LOGGER = logging.getLogger("sendspin-mpris-proxy")


async def _run():
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

    # Connect to the system bus
    _LOGGER.info("Connecting to system bus.")
    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

    # Construct and export MPRIS interfaces
    _LOGGER.info("Exporting MediaPlayer2 interface.")
    mediaplayer2 = MediaPlayer2Interface()
    bus.export("/org/mpris/MediaPlayer2", mediaplayer2)

    _LOGGER.info("Exporting MediaPlayer2.Player interface.")
    player = MediaPlayer2PlayerInterface()
    bus.export("/org/mpris/MediaPlayer2", player)

    # Acquire our friendly name
    name = f"org.mpris.MediaPlayer2.sendspin_proxy.pid_{os.getpid()}"
    _LOGGER.info(f"Requesting friendly name '{name}' on bus.")
    await bus.request_name(name)

    # Create the named pipe
    fifo = "/var/run/sendspin-mpris-proxy"
    try:
        os.remove(fifo)
    except FileNotFoundError:
        pass
    os.mkfifo(fifo)
    os.chmod(
        fifo,
        stat.S_IRUSR
        | stat.S_IWUSR
        | stat.S_IRGRP
        | stat.S_IWGRP
        | stat.S_IROTH
        | stat.S_IWOTH,
    )

    while True:
        # Blocking IO should be ok since we don't need to interact
        # with the DBus until we get an update
        with open(fifo, mode="r") as f:
            contents = f.read()

        matches = re.match("Playback Status: (\\w+)", contents)
        if matches is None:
            continue

        status = matches.group(1)
        _LOGGER.info(f"Set Playback Status: {status}")
        player.playback_status = status

        # Sleep to allow async tasks to run before blocking again
        # TODO might want to re-eval aiofiles
        await asyncio.sleep(1)


def main():
    try:
        asyncio.run(_run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
