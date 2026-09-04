import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from scores import load_high_scores

class HighScoresView(Gtk.Overlay):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        # Background Canvas for Soft Green Theme
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.on_draw)
        self.add(self.drawing_area)
        
        # UI Layout Container over Background Canvas
        overlay_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        overlay_box.set_border_width(30)
        
        # Header Title
        lbl_title = Gtk.Label()
        lbl_title.set_markup("<span font='24' weight='bold' foreground='#ffffff'>🏆 High Scores</span>")
        overlay_box.pack_start(lbl_title, False, False, 10)
        
        # Leaderboard Box Container
        scores_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        scores_box.set_border_width(20)
        
        scores = load_high_scores()
        if not scores:
            lbl_none = Gtk.Label()
            lbl_none.set_markup("<span font='13' style='italic' foreground='#e0e0e0'>No high scores recorded yet!</span>")
            scores_box.pack_start(lbl_none, True, True, 20)
        else:
            for rank, entry in enumerate(scores, 1):
                initials = entry.get("initials", "AAA")
                score = entry.get("score", 0)
                
                row_lbl = Gtk.Label()
                row_lbl.set_alignment(0.5, 0.5)
                
                # Gold for #1, clean white/light-gray text for readability
                rank_str = f"<span foreground='#f1c40f'>#{rank:<2}</span>" if rank == 1 else f"<span foreground='#d0d0d0'>#{rank:<2}</span>"
                
                row_lbl.set_markup(
                    f"<span font='15' weight='bold' foreground='#ffffff'>"
                    f"{rank_str}   <span foreground='#ffffff'>{initials}</span>   —   "
                    f"<span foreground='#ffffff'>{score:04d} pts</span>"
                    f"</span>"
                )
                scores_box.pack_start(row_lbl, False, False, 2)
                
        overlay_box.pack_start(scores_box, True, True, 0)
        
        # Back Button
        btn_back = Gtk.Button(label="Back to Menu")
        btn_back.set_size_request(160, 40)
        btn_back.connect("clicked", lambda x: self.main_window.show_menu())
        
        btn_center_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        btn_center_box.pack_start(btn_back, True, False, 0)
        overlay_box.pack_start(btn_center_box, False, False, 10)
        
        self.add_overlay(overlay_box)

    def on_draw(self, widget, cr):
        alloc = widget.get_allocation()
        
        # Outer Soft Sage Green Window Background (#2a4d36)
        cr.set_source_rgb(0.16, 0.30, 0.21)
        cr.paint()
        
        # Inner Dark Forest Green Card Panel (#13261a)
        card_margin_x = 40
        card_margin_y = 20
        
        rect_x = card_margin_x
        rect_y = card_margin_y
        rect_w = alloc.width - (2 * card_margin_x)
        rect_h = alloc.height - (2 * card_margin_y)
        
        cr.rectangle(rect_x, rect_y, rect_w, rect_h)
        cr.set_source_rgb(0.07, 0.15, 0.10)
        cr.fill_preserve()
        
        # Soft Green Accent Border Outline (#2a663f)
        cr.set_source_rgb(0.16, 0.40, 0.25)
        cr.set_line_width(2)
        cr.stroke()
