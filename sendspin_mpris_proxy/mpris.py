from dbus_fast import PropertyAccess
from dbus_fast.service import ServiceInterface, dbus_property

from .const import PlaybackStatus


class MediaPlayer2Interface(ServiceInterface):
    """MPRIS MediaPlayer2 Interface"""

    def __init__(self) -> None:
        super().__init__("org.mpris.MediaPlayer2")

    # Indicate we can't be controlled in any way
    @dbus_property(name="CanQuit", access=PropertyAccess.READ)
    def can_quit(self) -> "b":
        return False

    @dbus_property(name="CanSetFullscreen", access=PropertyAccess.READ)
    def can_set_fullscreen(self) -> "b":
        return False

    @dbus_property(name="CanRaise", access=PropertyAccess.READ)
    def can_raise(self) -> "b":
        return False

    @dbus_property(name="HasTrackList", access=PropertyAccess.READ)
    def has_track_list(self) -> "b":
        return False

    @dbus_property(name="Identity", access=PropertyAccess.READ)
    def identity(self) -> "s":
        return "MPRIS-Proxy"


class MediaPlayer2PlayerInterface(ServiceInterface):
    """MPRIS MediaPlayer2 Player Interface"""

    def __init__(self) -> None:
        super().__init__("org.mpris.MediaPlayer2.Player")

        self._playback_status = PlaybackStatus.STOPPED

    # Supported properties
    @dbus_property(name="PlaybackStatus", access=PropertyAccess.READ)
    def playback_status(self) -> "s":
        return self._playback_status

    @playback_status.setter
    def playback_status(self, status: PlaybackStatus) -> None:
        if self._playback_status == status:
            return

        self._playback_status = status
        self.emit_properties_changed({"PlaybackStatus": self._playback_status})

    # Indicate we can't be controlled in any way
    @dbus_property(name="CanControl", access=PropertyAccess.READ)
    def can_control(self) -> "b":
        return False

    @dbus_property(name="CanGoNext", access=PropertyAccess.READ)
    def can_go_next(self) -> "b":
        return False

    @dbus_property(name="CanGoPrevious", access=PropertyAccess.READ)
    def can_go_previous(self) -> "b":
        return False

    @dbus_property(name="CanPlay", access=PropertyAccess.READ)
    def can_play(self) -> "b":
        return False

    @dbus_property(name="CanPause", access=PropertyAccess.READ)
    def can_pause(self) -> "b":
        return False

    @dbus_property(name="CanSeek", access=PropertyAccess.READ)
    def can_seek(self) -> "b":
        return False
