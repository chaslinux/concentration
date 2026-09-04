import os
import wave
import math
import struct
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

class SoundManager:
    def __init__(self, sounds_dir="assets/sounds"):
        self.sounds_dir = sounds_dir
        os.makedirs(self.sounds_dir, exist_ok=True)
        self._ensure_default_sounds()
        
    def _create_wav(self, filename, duration_sec, freq_fn):
        """Generates simple synth wave tones if sound files don't exist."""
        filepath = os.path.join(self.sounds_dir, filename)
        if os.path.exists(filepath):
            return filepath

        sample_rate = 44100
        n_samples = int(sample_rate * duration_sec)
        
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            samples = []
            for i in range(n_samples):
                t = i / sample_rate
                freq = freq_fn(t)
                # Envelope decay to avoid clicks
                envelope = max(0.0, 1.0 - (t / duration_sec))
                val = int(32767 * 0.3 * envelope * math.sin(2 * math.pi * freq * t))
                samples.append(struct.pack('<h', val))
                
            wav_file.writeframes(b''.join(samples))
        return filepath

    def _ensure_default_sounds(self):
        """Creates procedural chimes/clicks so the game works out-of-the-box."""
        # 1. Flip sound (quick high click)
        self._create_wav("flip.wav", 0.08, lambda t: 600 - t * 2000)
        
        # 2. Match sound (pleasant ascending arpeggio)
        self._create_wav("match.wav", 0.3, lambda t: 523.25 if t < 0.1 else (659.25 if t < 0.2 else 783.99))
        
        # 3. Mismatch sound (low double buzz)
        self._create_wav("mismatch.wav", 0.25, lambda t: 160.0 if (t < 0.1 or t > 0.15) else 0.0)
        
        # 4. Win sound (fanfare chime)
        self._create_wav("win.wav", 0.6, lambda t: 440 + (t * 800))

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
sound = SoundManager()
