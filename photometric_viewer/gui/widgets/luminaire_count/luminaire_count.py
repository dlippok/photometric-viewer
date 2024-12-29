from gi.repository.Adw import ActionRow
from gi.repository.Gtk import ListBox, SelectionMode, Label


class LuminaireCountListBox(ListBox):
    def __init__(self):
        super().__init__(
            css_classes=["boxed-list"],
            selection_mode=SelectionMode.NONE
        )

        self.count_label = Label()
        luminaire_count_row = ActionRow(title=_("Required number of luminaires"))
        luminaire_count_row.add_suffix(self.count_label)
        self.append(luminaire_count_row)

        self.achieved_illuminance_label = Label()
        achieved_illuminance_row = ActionRow(title=_("Achieved illuminance"))
        achieved_illuminance_row.add_suffix(self.achieved_illuminance_label)
        self.append(achieved_illuminance_row)

        self.set_count(None)
        self.set_achieved_illuminance(None)

    def set_count(self, count: int | None):
        if count is not None:
            self.count_label.set_label(f"{count}")
        else:
            self.count_label.set_label(_("Unknown"))

    def set_achieved_illuminance(self, illuminance: float | None):
        if illuminance is not None:
            self.achieved_illuminance_label.set_label(f"{illuminance:.1f}")
        else:
            self.achieved_illuminance_label.set_label(_("Unknown"))

