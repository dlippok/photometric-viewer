from gi.repository import Gtk
from gi.repository.GtkSource import Language, View
from gi.repository.Pango import EllipsizeMode

from gui.widgets.source.goto_line_popover import GotoLinePopover


class StatusBar(Gtk.Box):
    def __init__(self, connected_view: View):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            css_classes=["statusbar"],
        )

        self.filename_label = Gtk.Label(margin_start=6,  margin_top=6, margin_bottom=6, ellipsize=EllipsizeMode.MIDDLE)
        self.unsaved_label = Gtk.Label(label="*", margin_end=6)
        self.language_label = Gtk.Label(margin_start=6, margin_end=6, margin_top=6, margin_bottom=6)
        self.cursor_position_label = Gtk.Label()
        self.goto_line_popover = GotoLinePopover(connected_view)
        self.goto_line_popover.connect("show", self.on_goto_line_popover_show)

        self.cursor_positon_button = Gtk.MenuButton(
            popover=self.goto_line_popover,
            direction=Gtk.ArrowType.UP,
            css_classes=["flat", "round"]
        )
        self.cursor_positon_button.set_child(self.cursor_position_label)
        self.cursor_positon_button.set_popover(self.goto_line_popover)

        self.append(Gtk.Separator())
        self.append(Gtk.Image(icon_name="text-x-generic-symbolic", margin_start=12))
        self.append(self.filename_label)
        self.append(self.unsaved_label)

        self.append(Gtk.Box(hexpand=True))

        self.append(self.cursor_positon_button)
        self.append(Gtk.Image(icon_name="text-editor-symbolic", margin_start=12))
        self.append(self.language_label)

        self.set_source_language(None)
        self.set_cursor_position(1, 1)
        self.set_filename(None)
        self.set_unsaved(False)

    def set_filename(self, filename: str | None):
        self.filename_label.set_label(filename or _("Unnamed file"))

    def set_unsaved(self, is_unsaved: bool):
        self.unsaved_label.set_label("*" if is_unsaved else "")

    def on_goto_line_popover_show(self, *args):
        self.goto_line_popover.goto_line_entry.set_text(self.cursor_position_label.get_text())
        self.goto_line_popover.goto_line_entry.select_region(0, -1)

    def set_source_language(self, lang: Language | None):
        if lang:
            self.language_label.set_label(lang.get_name())
        else:
            self.language_label.set_label(_("Unknown"))

    def set_cursor_position(self, line: int, column: int):
        self.goto_line_popover.set_cursor_position(line, column)
        self.cursor_position_label.set_label(f"{line}:{column}")

