import time
import random
import os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Rsvg', '2.0')
from gi.repository import Gtk, Gdk, GLib, Rsvg

import config
from scores import save_high_score

class Card:
    def __init__(self, icon_name, index):
        self.icon_name = icon_name
        self.index = index
        self.is_flipped = False
        self.is_matched = False
        self.is_hidden = False
        self.svg_handle = None
        
        path = os.path.join(config.ICON_DIR, icon_name)
        if os.path.exists(path):
            try:
                self.svg_handle = Rsvg.Handle.new_from_file(path)
            except Exception:
                self.svg_handle = None

class ConcentrationBoard(Gtk.Box):
    def __init__(self, main_window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.main_window = main_window
        
        self.score = 0
        self.time_remaining = config.GAME_TIME
        self.selected_cards = []
        self.focused_index = 0
        self.lock_input = False
        self.flip_timer_id = None
        
        # Grid margins & gaps
        self.margin_pad = 20
        self.card_gap = 8
        
        # Random card selection
        random.seed(time.time())
        selected_icons = random.sample(config.AVAILABLE_ICONS, config.TOTAL_MATCHES)
        card_icons = selected_icons * 2
        random.shuffle(card_icons)
        
        self.cards = [Card(icon, i) for i, icon in enumerate(card_icons)]
        
        # Header UI
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        
        self.lbl_score = Gtk.Label()
        self.lbl_score.set_alignment(0.5, 0.5)
        self.lbl_score.set_markup("<span font='20' weight='bold' foreground='#2ecc71'>Score: 0000</span>")
        
        self.lbl_timer = Gtk.Label()
        self.lbl_timer.set_alignment(0.5, 0.5)
        self.update_timer_label()
        
        header.pack_start(self.lbl_score, True, True, 10)
        header.pack_start(self.lbl_timer, True, True, 10)
        self.pack_start(header, False, False, 10)
        
        # Drawing Area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_can_focus(True)
        self.drawing_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.KEY_PRESS_MASK)
        
        self.drawing_area.connect("draw", self.on_draw)
        self.drawing_area.connect("button-press-event", self.on_click)
        self.drawing_area.connect("key-press-event", self.on_key_press)
        
        self.pack_start(self.drawing_area, True, True, 0)
        
        # Start Countdown Loop
        self.timer_source_id = GLib.timeout_add_seconds(1, self.on_tick)
        self.drawing_area.grab_focus()

    def update_score(self, points):
        self.score += points
        self.lbl_score.set_markup(f"<span font='20' weight='bold' foreground='#2ecc71'>Score: {self.score:04d}</span>")

    def update_timer_label(self):
        mins, secs = divmod(self.time_remaining, 60)
        color = "#e74c3c" if self.time_remaining <= 30 else "#f39c12"
        self.lbl_timer.set_markup(f"<span font='20' weight='bold' foreground='{color}'>Time: {mins:02d}:{secs:02d}</span>")

    def on_tick(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_timer_label()
            return True
        else:
            self.end_game("Time's Up!")
            return False

    def on_draw(self, widget, cr):
        alloc = widget.get_allocation()
        
        # Calculate grid bounds
        grid_w = alloc.width - (2 * self.margin_pad)
        grid_h = alloc.height - (2 * self.margin_pad)
        
        card_w = grid_w / config.COLS
        card_h = grid_h / config.ROWS
        
        # Soft Green Application Background
        cr.set_source_rgb(0.16, 0.30, 0.21)
        cr.paint()
        
        for i, card in enumerate(self.cards):
            if card.is_hidden:
                continue

            r, c = divmod(i, config.COLS)
            x = self.margin_pad + (c * card_w) + (self.card_gap / 2)
            y = self.margin_pad + (r * card_h) + (self.card_gap / 2)
            w = card_w - self.card_gap
            h = card_h - self.card_gap
            
            # Card Base Shape
            cr.rectangle(x, y, w, h)
            
            if card.is_flipped or card.is_matched:
                # Yellow Front Face
                cr.set_source_rgb(0.95, 0.61, 0.07)
                cr.fill_preserve()
                
                # Darker yellow border
                cr.set_source_rgb(0.75, 0.45, 0.05)
                cr.set_line_width(2)
                cr.stroke()
                
                # Large, Centered SVG Icon
                if card.svg_handle:
                    cr.save()
                    
                    dim_obj = card.svg_handle.get_dimensions()
                    svg_w, svg_h = dim_obj.width, dim_obj.height
                    
                    if svg_w > 0 and svg_h > 0:
                        scale = min(w / svg_w, h / svg_h) * 0.85
                        rendered_w = svg_w * scale
                        rendered_h = svg_h * scale
                        
                        offset_x = x + (w - rendered_w) / 2.0
                        offset_y = y + (h - rendered_h) / 2.0
                        
                        cr.translate(offset_x, offset_y)
                        cr.scale(scale, scale)
                        card.svg_handle.render_cairo(cr)
                        
                    cr.restore()
            else:
                # Back side background: Forest green
                cr.set_source_rgb(0.15, 0.55, 0.30)
                cr.fill_preserve()
                
                # Hatch Marks Overlay
                cr.save()
                cr.clip()
                cr.set_source_rgba(0.08, 0.35, 0.18, 0.6)
                cr.set_line_width(2)
                for line_x in range(int(x - h), int(x + w + h), 12):
                    cr.move_to(line_x, y)
                    cr.line_to(line_x + h, y + h)
                cr.stroke()
                cr.restore()
                
                cr.set_source_rgb(0.10, 0.40, 0.20)
                cr.set_line_width(2)
                cr.stroke()
            
            # Keyboard Focus Highlight
            if i == self.focused_index and not card.is_hidden:
                cr.rectangle(x - 2, y - 2, w + 4, h + 4)
                cr.set_source_rgb(1.0, 1.0, 1.0)
                cr.set_line_width(3)
                cr.stroke()

    def select_card(self, index):
        if self.lock_input:
            return
        card = self.cards[index]
        if card.is_flipped or card.is_matched or card.is_hidden:
            return
            
        card.is_flipped = True
        self.selected_cards.append(card)
        self.drawing_area.queue_draw()
        
        if len(self.selected_cards) == 2:
            self.lock_input = True
            c1, c2 = self.selected_cards
            if c1.icon_name == c2.icon_name:
                c1.is_matched = True
                c2.is_matched = True
                self.update_score(100 + self.time_remaining)
                
                # Instantly mark matched cards hidden
                c1.is_hidden = True
                c2.is_hidden = True
                self.selected_cards = []
                self.lock_input = False
                self.drawing_area.queue_draw()

                # Trigger victory dialog immediately when all are matched
                if all(c.is_hidden for c in self.cards):
                    GLib.idle_add(self.end_game, "🎉 YOU WIN!")
            else:
                self.flip_timer_id = GLib.timeout_add_seconds(config.FLIP_TIMEOUT, self.unflip_selected)

    def unflip_selected(self):
        for card in self.selected_cards:
            card.is_flipped = False
        self.selected_cards = []
        self.lock_input = False
        self.drawing_area.queue_draw()
        self.flip_timer_id = None
        return False

    def on_click(self, widget, event):
        alloc = widget.get_allocation()
        grid_w = alloc.width - (2 * self.margin_pad)
        grid_h = alloc.height - (2 * self.margin_pad)
        
        click_x = event.x - self.margin_pad
        click_y = event.y - self.margin_pad
        
        if 0 <= click_x < grid_w and 0 <= click_y < grid_h:
            card_w = grid_w / config.COLS
            card_h = grid_h / config.ROWS
            
            c = int(click_x // card_w)
            r = int(click_y // card_h)
            idx = r * config.COLS + c
            
            if 0 <= idx < config.TOTAL_CARDS:
                self.focused_index = idx
                self.select_card(idx)

    def on_key_press(self, widget, event):
        keyval = event.keyval
        r, c = divmod(self.focused_index, config.COLS)
        
        if keyval == Gdk.KEY_Left and c > 0:
            self.focused_index -= 1
        elif keyval == Gdk.KEY_Right and c < config.COLS - 1:
            self.focused_index += 1
        elif keyval == Gdk.KEY_Up and r > 0:
            self.focused_index -= config.COLS
        elif keyval == Gdk.KEY_Down and r < config.ROWS - 1:
            self.focused_index += config.COLS
        elif keyval in (Gdk.KEY_Return, Gdk.KEY_space):
            self.select_card(self.focused_index)
            
        self.drawing_area.queue_draw()

    def end_game(self, title_text):
        dialog = Gtk.Dialog(title="Game Finished", parent=self.main_window, flags=0)
        dialog.set_default_size(360, 240)
        
        btn_save = dialog.add_button("Save Score", Gtk.ResponseType.OK)
        dialog.set_default_response(Gtk.ResponseType.OK)
        
        box = dialog.get_content_area()
        box.set_spacing(12)
        box.set_border_width(20)
        
        # Heading Label
        lbl_title = Gtk.Label()
        lbl_title.set_markup(f"<span font='22' weight='bold' foreground='#2ecc71'>{title_text}</span>")
        box.pack_start(lbl_title, False, False, 0)
        
        # Final Score Label
        lbl_score = Gtk.Label()
        lbl_score.set_markup(f"<span font='14' weight='bold'>Final Score: <span foreground='#f39c12'>{self.score}</span></span>")
        box.pack_start(lbl_score, False, False, 0)
        
        # Instructions
        lbl_prompt = Gtk.Label()
        lbl_prompt.set_markup("<span font='11'>Enter your <b>3 Initials</b> for the Leaderboard:</span>")
        lbl_prompt.set_line_wrap(True)
        box.pack_start(lbl_prompt, False, False, 4)
        
        # 3-Letter Entry Input
        entry = Gtk.Entry()
        entry.set_max_length(3)
        entry.set_alignment(0.5)
        entry.set_placeholder_text("AAA")
        entry.set_property("width-chars", 6)
        box.pack_start(entry, False, False, 6)
        
        dialog.show_all()
        dialog.run()
        
        initials = entry.get_text().strip().upper() or "AAA"
        save_high_score(initials, self.score)
        dialog.destroy()
        
        self.main_window.show_high_scores()
        return False
