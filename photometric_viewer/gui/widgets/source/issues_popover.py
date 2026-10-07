from typing import List

from gi.repository import Gtk, Adw
from gi.repository.GtkSource import View

from photometric_viewer.gui.utils.issues.issue_translation import get_translations
from photometric_viewer.photometry.validation import ValidationIssueBase, Severity


class IssuesPopover(Gtk.Popover):
    def __init__(self, connected_view: View):
        super().__init__()
        self.connected_view = connected_view
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        box.append(
            Gtk.Label(
                label=_("Issues"),
                css_classes=["heading"],
                margin_top=12,
                margin_bottom=12
            )
        )

        self.issues_list = Gtk.ListBox(
            selection_mode=Gtk.SelectionMode.NONE,
            css_classes=['boxed-list'],
            width_request=400

        )

        scrolled_window = Gtk.ScrolledWindow(
            child=self.issues_list,
            vexpand=True,
            hscrollbar_policy=Gtk.PolicyType.NEVER,
            vscrollbar_policy=Gtk.PolicyType.AUTOMATIC,
            max_content_height=500,
            propagate_natural_height=True
        )

        box.append(scrolled_window)

        self.set_child(box)

    def update_issues(self, issues: List[ValidationIssueBase]) -> None:
        self.issues_list.remove_all()
        decorated_issues = [i for i in issues]
        decorated_issues.sort(key=lambda x: x.line_number)
        decorated_issues.sort(key=lambda x: x.severity.value)
        for issue in decorated_issues:
            row = self._create_list_item(issue)
            self.issues_list.append(row)

    def _create_list_item(self, issue: ValidationIssueBase) -> Adw.ActionRow:
        translations = get_translations(issue)

        row = Adw.ActionRow(
            title=translations.translation,
            css_classes=self._css_class(issue)
        )
        if translations.details:
            row.set_subtitle(translations.details)

        row.add_prefix(Gtk.Image(icon_name=self._icon_name(issue)))

        if issue.line_number is not None:
            row.add_suffix(
                Gtk.Label(
                    label=_("Line: ") + str(issue.line_number),
                )
            )
            row.set_activatable(True)
            row.connect('activated', lambda _: self._goto_line(issue.line_number))

        return row

    def _goto_line(self, number: int):
        try:
            buffer = self.connected_view.get_buffer()

            (_, iter) = buffer.get_iter_at_line_offset(
                max(number - 1, 0),
                0
            )
            buffer.place_cursor(iter)
            self.connected_view.scroll_to_iter(iter, within_margin=0.1, use_align=False, xalign=0, yalign=0.5)
        finally:
            self.connected_view.grab_focus()
            self.set_visible(False)

    @staticmethod
    def _icon_name(issue: ValidationIssueBase) -> str:
        match issue.severity:
            case Severity.ERROR:
                return "errors-symbolic"
            case Severity.WARNING:
                return "warnings-symbolic"
            case Severity.INFO:
                return "infos-symbolic"
            case Severity.STYLE:
                return "styles-symbolic"


    @staticmethod
    def _css_class(issue: ValidationIssueBase) -> List[str]:
        match issue.severity:
            case Severity.ERROR:
                return ["error"]
            case Severity.WARNING:
                return ["warning"]
            case _:
                return []

