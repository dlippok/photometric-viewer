from gi.repository.Adw import ActionRow
from gi.repository.Gtk import ListBox, SelectionMode, Label


class LuminaireCountListBox(ListBox):
    def __init__(self):
        super().__init__(
            css_classes=["boxed-list"],
            selection_mode=SelectionMode.NONE
        )

        self.result_label = Label()
        luminaire_count_row = ActionRow(title=_("Required number of luminaires"))
        luminaire_count_row.add_suffix(self.result_label)
        self.append(luminaire_count_row)

        self.set_count(None)

    def set_count(self, count: int | None):
        if count is not None:
            self.result_label.set_label(f"{count}")
        else:
            self.result_label.set_label(_("Unknown"))
