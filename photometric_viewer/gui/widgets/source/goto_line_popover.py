from gi.repository import Gtk
from gi.repository.GtkSource import View


class GotoLinePopover(Gtk.Popover):
    def __init__(self, connected_view: View):
        super().__init__()
        self.connected_view = connected_view
        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL
        )

        box.append(
            Gtk.Label(
                label=_("Go to line"),
                css_classes=["heading"],
                margin_top=12,
                margin_bottom=12
            )
        )

        goto_line_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL
        )

        self.goto_line_entry = Gtk.Entry(
            placeholder_text=_("line[:column]"),
            activates_default=True,
            margin_bottom=12,
            margin_start=12,
        )
        self.goto_line_entry.set_alignment(0.5)
        self.goto_line_entry.connect("changed", self.on_goto_line_text_changed)

        self.goto_line_button = Gtk.Button(
            label=_("Go to"),
            css_classes=["suggested-action"],
            margin_bottom=12,
            margin_start=6,
            margin_end=12
        )
        self.goto_line_button.connect('clicked', self.goto_line_button_clicked)

        goto_line_box.append(self.goto_line_entry)
        goto_line_box.append(self.goto_line_button)
        box.append(goto_line_box)

        self.set_default_widget(self.goto_line_button)
        self.set_child(box)

    def set_cursor_position(self, line: int, column: int):
        self.goto_line_entry.set_text(f"{line}:{column}")

    def goto_line_button_clicked(self, *args):
        value = self.goto_line_entry.get_text()

        if value.strip() == '':
            self.connected_view.grab_focus()
            self.set_visible(False)
            return

        try:
            values = value.split(":")
            line = int(values[0]) - 1
            column = int(values[1]) - 1 if len(values) > 1 else 0
            buffer = self.connected_view.get_buffer()
            (_, iter) = buffer.get_iter_at_line_offset(
                max(line, 0),
                max(column, 0)
            )
            buffer.place_cursor(iter)
        finally:
            self.connected_view.grab_focus()
            self.set_visible(False)

    def on_goto_line_text_changed(self, entry: Gtk.Entry):
        current_text = entry.get_text()
        allowed_chars = "1234567890:"

        if all(char in allowed_chars for char in current_text):
            self.goto_line_button.set_sensitive(True)
        else:
            self.goto_line_button.set_sensitive(False)
