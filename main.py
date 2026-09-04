import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ui.menu import MainMenu
from ui.game_board import ConcentrationBoard
from ui.high_scores import HighScoresView

class ConcentrationWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Concentration - Papirus Icon Edition")
        self.set_default_size(900, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", Gtk.main_quit)

        self.current_view = None
        self.show_menu()

    def clear_view(self):
        if self.current_view:
            self.remove(self.current_view)
            self.current_view.destroy()
            self.current_view = None

    def show_menu(self):
        self.clear_view()
        self.current_view = MainMenu(self)
        self.add(self.current_view)
        self.show_all()

    def start_game(self):
        self.clear_view()
        self.current_view = ConcentrationBoard(self)
        self.add(self.current_view)
        self.show_all()

    def show_high_scores(self):
        self.clear_view()
        self.current_view = HighScoresView(self)
        self.add(self.current_view)
        self.show_all()

if __name__ == "__main__":
    win = ConcentrationWindow()
    Gtk.main()
