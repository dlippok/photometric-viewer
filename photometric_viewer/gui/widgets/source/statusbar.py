from gi.repository import Gtk
from gi.repository.GtkSource import Language, View
from gi.repository.Pango import EllipsizeMode

from typing import List

from photometric_viewer.gui.widgets.source.issues_popover import IssuesPopover
from photometric_viewer.gui.widgets.source.goto_line_popover import GotoLinePopover
from photometric_viewer.model.luminaire import FileFormat
from photometric_viewer.photometry.validation import ValidationIssueBase, Severity


class StatusBar(Gtk.Box):
    def __init__(self, connected_view: View):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            css_classes=["statusbar"],
            margin_start=12,
            margin_end=12,
            margin_top=3,
            margin_bottom=3,
        )

        self.filename_label = Gtk.Label(ellipsize=EllipsizeMode.MIDDLE)
        self.unsaved_label = Gtk.Label(label="*", margin_end=6)
        self.language_label = Gtk.Label()
        self.cursor_position_label = Gtk.Label()
        self.goto_line_popover = GotoLinePopover(connected_view)
        self.goto_line_popover.connect("show", self.on_goto_line_popover_show)

        self.issues_popover = IssuesPopover(connected_view)

        self.cursor_positon_button = Gtk.MenuButton(
            popover=self.goto_line_popover,
            direction=Gtk.ArrowType.UP,
            css_classes=["flat", "round"]
        )
        self.cursor_positon_button.set_child(self.cursor_position_label)

        self.issues_button = Gtk.MenuButton(
            popover=self.issues_popover,
            direction=Gtk.ArrowType.UP,
            css_classes=["flat", "round"]
        )

        self.append(Gtk.Image(icon_name="text-x-generic-symbolic", margin_end=6))
        self.append(self.filename_label)
        self.append(self.unsaved_label)

        self.append(Gtk.Separator(css_classes=["spacer"], margin_end=12))
        self.append(self.issues_button)

        self.append(Gtk.Box(hexpand=True))

        self.append(Gtk.Separator(css_classes=["spacer"], margin_end=12))
        self.append(self.cursor_positon_button)

        self.append(Gtk.Separator(css_classes=["spacer"], margin_end=12))
        self.append(Gtk.Image(icon_name="text-editor-symbolic", margin_end=6))
        self.append(self.language_label)

        self.update_issues([])
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

    def set_source_language(self, file_format: FileFormat | None):
        match file_format:
            case FileFormat.IES_LM63_1995:
                self.language_label.set_label("ANSI/IESNA LM-63-1995")
            case FileFormat.IES_LM63_2002:
                self.language_label.set_label("ANSI/IESNA LM-63-2002")
            case FileFormat.IES_LM63_1991:
                self.language_label.set_label("ANSI/IESNA LM-63-1991")
            case FileFormat.EULUMDAT:
                self.language_label.set_label("EULUMDAT")
            case _:
                self.language_label.set_label(_("Unknown"))

    def update_issues(self, issues: List[ValidationIssueBase]):
        n_errors = len([i for i in issues if i.severity == Severity.ERROR])
        n_warnings = len([i for i in issues if i.severity == Severity.WARNING])
        n_info = len([i for i in issues if i.severity == Severity.INFO])
        n_style = len([i for i in issues if i.severity == Severity.STYLE])

        issues_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        total_issues = n_style + n_info + n_warnings + n_errors
        if total_issues == 0:
            self.issues_button.set_visible(False)
        else:
            self.issues_button.set_visible(True)
            remaining_issues = total_issues
            if n_errors:
                issues_box.append(Gtk.Image(icon_name="errors-symbolic", margin_end=6))
                issues_box.append(Gtk.Label(label=str(n_errors)))
                remaining_issues -= n_errors

                if remaining_issues:
                    issues_box.append(Gtk.Separator(css_classes=["spacer"], margin_end=12))

            if n_warnings:
                issues_box.append(Gtk.Image(icon_name="warnings-symbolic", margin_end=6))
                issues_box.append(Gtk.Label(label=str(n_warnings)))
                remaining_issues -= n_warnings

                if remaining_issues:
                    issues_box.append(Gtk.Separator(css_classes=["spacer"], margin_end=12))

            if n_info:
                issues_box.append(Gtk.Image(icon_name="infos-symbolic", margin_end=6))
                issues_box.append(Gtk.Label(label=str(n_info)))
                remaining_issues -= n_info

                if remaining_issues:
                    issues_box.append(Gtk.Separator(css_classes=["spacer"], margin_end=12))

            if n_style:
                issues_box.append(Gtk.Image(icon_name="styles-symbolic", margin_end=6))
                issues_box.append(Gtk.Label(label=str(n_style)))

        if issues:
            print(f"Found {len(issues)} issues:")
            for issue in issues:
                print(f"[{issue.line_number}] [{issue.severity}]: {issue}")
        else:
            print("No issues found")

        self.issues_button.set_child(issues_box)

    def set_cursor_position(self, line: int, column: int):
        self.goto_line_popover.set_cursor_position(line, column)
        self.cursor_position_label.set_label(f"{line}:{column}")

