import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainMenu(Gtk.Box):
    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.main_window = main_window
        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)

        title = Gtk.Label()
        title.set_markup("<span font='28' weight='bold' foreground='#3498db'>CONCENTRATION</span>")
        self.pack_start(title, False, False, 20)

        btn_play = Gtk.Button(label="Play Game")
        btn_play.set_size_request(200, 50)
        btn_play.connect("clicked", lambda x: self.main_window.start_game())
        self.pack_start(btn_play, False, False, 0)

        btn_scores = Gtk.Button(label="High Scores")
        btn_scores.set_size_request(200, 50)
        btn_scores.connect("clicked", lambda x: self.main_window.show_high_scores())
        self.pack_start(btn_scores, False, False, 0)

        btn_exit = Gtk.Button(label="Exit")
        btn_exit.set_size_request(200, 50)
        btn_exit.connect("clicked", lambda x: Gtk.main_quit())
        self.pack_start(btn_exit, False, False, 0)
