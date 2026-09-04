import sys
import os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk

from ui.menu import MenuView
from ui.game_board import ConcentrationBoard
from ui.high_scores import HighScoresView

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    if os.path.exists(css_path):
        provider = Gtk.CssProvider()
        provider.load_from_path(css_path)
        
        screen = Gdk.Screen.get_default()
        priority = Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        Gtk.StyleContext.add_provider_for_screen(screen, provider, priority)

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Concentration")
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", Gtk.main_quit)
        
        # Renamed self.container -> self.main_box to avoid reserved attribute name
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.main_box)
        
        self.show_menu()

    def clear_container(self):
        for child in self.main_box.get_children():
            self.main_box.remove(child)

    def show_menu(self):
        self.clear_container()
        menu_view = MenuView(self)
        self.main_box.pack_start(menu_view, True, True, 0)
        self.show_all()

    def start_game(self):
        self.clear_container()
        game_view = ConcentrationBoard(self)
        self.main_box.pack_start(game_view, True, True, 0)
        self.show_all()

    def show_high_scores(self):
        self.clear_container()
        scores_view = HighScoresView(self)
        self.main_box.pack_start(scores_view, True, True, 0)
        self.show_all()

if __name__ == "__main__":
    load_css()
    app = MainWindow()
    app.show_all()
    Gtk.main()
