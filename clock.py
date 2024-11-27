import gi
gi.require_version("Gtk", "3.0")
import math
from datetime import datetime
from gi.repository import Gtk, GLib, Pango
import cairo


class AnalogClock(Gtk.Window):
    def __init__(self):
        super().__init__(title="Analog Clock")
        self.set_default_size(100, 100)
        self.set_resizable(False)
        self.set_skip_taskbar_hint(True)
        self.set_decorated(False)
        self.set_keep_below(True)


        self.connect("destroy", Gtk.main_quit)


        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.on_draw)
        self.add(self.drawing_area)


        # Update the clock every second
        GLib.timeout_add(1000, self.update_clock)
        self.menu = Gtk.Menu()
    
        close_item = Gtk.MenuItem(label="close")
        close_item.connect("activate", Gtk.main_quit)
        self.menu.append(close_item)

        self.menu.show_all()

        self.connect("button-press-event", self.open_menu)

    def update_clock(self):
        self.drawing_area.queue_draw()
        return True


    def on_draw(self, widget, cr):
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        radius = min(width, height) / 2 - 10


        # Center of the clock
        center_x = width / 2
        center_y = height / 2


        # Get current time
        now = datetime.now()
        seconds = now.second
        minutes = now.minute + seconds / 60.0
        hours = now.hour % 12 + minutes / 60.0


        # Draw clock face
        cr.set_source_rgb(0.9, 0.9, 0.9) # White background
        cr.paint()


        # Draw clock border
        cr.set_source_rgb(0.20, 0.20, 0.20) # Black color
        cr.set_line_width(10)
        cr.arc(center_x, center_y, radius, 0, 2 * math.pi)
        cr.stroke()


        # Draw hour hand
        hour_angle = (hours / 12) * 2 * math.pi - math.pi / 2
        hour_length = radius * 0.5
        cr.set_line_width(8)
        cr.move_to(center_x, center_y)
        cr.line_to(center_x + hour_length * math.cos(hour_angle), center_y + hour_length * math.sin(hour_angle))
        cr.stroke()


        # Draw minute hand
        minute_angle = (minutes / 60) * 2 * math.pi - math.pi / 2
        minute_length = radius * 0.75
        cr.set_line_width(5)
        cr.move_to(center_x, center_y)
        cr.line_to(center_x + minute_length * math.cos(minute_angle), center_y + minute_length * math.sin(minute_angle))
        cr.stroke()


        # Draw second hand
        second_angle = (seconds / 60) * 2 * math.pi - math.pi / 2
        second_length = radius * 0.9
        cr.set_source_rgb(1, 0, 0) # Red color for seconds
        cr.set_line_width(2)
        cr.move_to(center_x, center_y)
        cr.line_to(center_x + second_length * math.cos(second_angle), center_y + second_length * math.sin(second_angle))
        cr.stroke()


        # Draw tick marks and numbers
        cr.set_source_rgb(0, 0, 0)
        for i in range(12):
            angle = (i / 12) * 2 * math.pi - math.pi / 0.17135555555
            start_x = center_x + (radius - 5) * math.cos(angle)
            start_y = center_y + (radius - 5) * math.sin(angle)
            end_x = center_x + (radius - 10) * math.cos(angle)
            end_y = center_y + (radius - 10) * math.sin(angle)
            cr.set_line_width(2)
            cr.move_to(start_x, start_y)
            cr.line_to(end_x, end_y)
            cr.stroke()


            # Draw the numbers
            cr.save()
            cr.translate(center_x, center_y)
            cr.rotate(angle) # Rotate to the correct position
            cr.move_to(-6, -(radius - 30)) # Position the number
            cr.set_source_rgb(0, 0, 0) # Black color for numbers
            cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cr.set_font_size(13)
            cr.show_text(str(i + 1)) # Draw the number
            cr.restore()

    def open_menu(self, w, event):
        if event.button == 3: # Right-click
            self.menu.popup_at_pointer(event)


if __name__ == "__main__":
    clock = AnalogClock()
    clock.show_all()
    Gtk.main()