import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class MenuView(Gtk.Box):
    """Main menu view for the Concentration card game styled to match High Scores and Game Board."""

    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.main_window = main_window

        # Drawing area background to match game felt green (#162d1e)
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.on_draw_bg)

        # Overlay structure so UI controls draw over custom canvas background
        overlay = Gtk.Overlay()
        overlay.add(self.drawing_area)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=25)
        content_box.set_valign(Gtk.Align.CENTER)
        content_box.set_halign(Gtk.Align.CENTER)
        content_box.set_margin_top(40)
        content_box.set_margin_bottom(40)

        # Decorative Card Preview Widget
        preview_area = Gtk.DrawingArea()
        preview_area.set_size_request(200, 70)
        preview_area.connect("draw", self.on_draw_preview)
        content_box.pack_start(preview_area, False, False, 0)

        # Main Title
        lbl_title = Gtk.Label()
        lbl_title.set_markup(
            "<span font='36' weight='bold' foreground='#2ecc71'>CONCENTRATION</span>"
        )
        content_box.pack_start(lbl_title, False, False, 0)

        # Subtitle
        lbl_subtitle = Gtk.Label()
        lbl_subtitle.set_markup(
            "<span font='13' weight='medium' foreground='#f39c12'>THE CLASSIC MEMORY MATCHING GAME</span>"
        )
        content_box.pack_start(lbl_subtitle, False, False, 0)

        # Menu Action Buttons Container
        btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        btn_box.set_halign(Gtk.Align.CENTER)

        btn_play = Gtk.Button(label="PLAY GAME")
        btn_play.set_size_request(220, 48)
        btn_play.connect("clicked", self.on_play_clicked)
        btn_box.pack_start(btn_play, False, False, 0)

        btn_scores = Gtk.Button(label="HIGH SCORES")
        btn_scores.set_size_request(220, 48)
        btn_scores.connect("clicked", self.on_high_scores_clicked)
        btn_box.pack_start(btn_scores, False, False, 0)

        btn_quit = Gtk.Button(label="QUIT GAME")
        btn_quit.set_size_request(220, 48)
        btn_quit.connect("clicked", self.on_quit_clicked)
        btn_box.pack_start(btn_quit, False, False, 0)

        content_box.pack_start(btn_box, False, False, 10)

        overlay.add_overlay(content_box)
        self.pack_start(overlay, True, True, 0)

    def on_draw_bg(self, widget, cr):
        """Draws dark forest green table backdrop."""
        cr.set_source_rgb(0.08, 0.17, 0.11)
        cr.paint()

    def on_draw_preview(self, widget, cr):
        """Draws two stylized card graphics at the top of the menu."""
        alloc = widget.get_allocation()
        center_x = alloc.width / 2.0
        center_y = alloc.height / 2.0

        card_w, card_h = 42, 58

        # Left Card (Back face)
        x1, y1 = center_x - 48, center_y - (card_h / 2.0)
        cr.rectangle(x1, y1, card_w, card_h)
        cr.set_source_rgb(0.15, 0.55, 0.30)
        cr.fill_preserve()
        cr.set_source_rgb(0.10, 0.40, 0.20)
        cr.set_line_width(2)
        cr.stroke()

        # Right Card (Front face - Gold)
        x2, y2 = center_x + 6, center_y - (card_h / 2.0)
        cr.rectangle(x2, y2, card_w, card_h)
        cr.set_source_rgb(0.95, 0.61, 0.07)
        cr.fill_preserve()
        cr.set_source_rgb(0.75, 0.45, 0.05)
        cr.set_line_width(2)
        cr.stroke()

        # Star on Front Card
        cr.save()
        cr.set_source_rgb(0.15, 0.25, 0.18)
        cr.arc(x2 + (card_w / 2.0), y2 + (card_h / 2.0), 8, 0, 2 * 3.14159)
        cr.fill()
        cr.restore()

    def on_play_clicked(self, button):
        self.main_window.start_game()

    def on_high_scores_clicked(self, button):
        self.main_window.show_high_scores()

    def on_quit_clicked(self, button):
        Gtk.main_quit()
