import os
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

class SoundManager:
    def __init__(self, sounds_dir):
        self.sounds_dir = sounds_dir

    def play(self, sound_name):
        """Plays a sound file using GStreamer playbin."""
        filepath = os.path.abspath(os.path.join(self.sounds_dir, f"{sound_name}.wav"))
        if not os.path.exists(filepath):
            return

        uri = f"file://{filepath}"
        player = Gst.ElementFactory.make("playbin", None)
        if player:
            player.set_property("uri", uri)
            player.set_state(Gst.State.PLAYING)

            # Bus watch to clean up pipeline after playback finishes
            bus = player.get_bus()
            def on_message(bus, message, user_data=None):
                t = message.type
                if t in (Gst.MessageType.EOS, Gst.MessageType.ERROR):
                    player.set_state(Gst.State.NULL)
                    return False
                return True
            
            bus.add_watch(0, on_message, None)

# Global sound instance
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "assets", "sounds")

sound = SoundManager(SOUNDS_DIR)
