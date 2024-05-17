from gi.repository import Gio


def action_entry(name: str, activate, parameter_type: str | None = None) -> Gio.ActionEntry:
    entry = Gio.ActionEntry
    entry.name = name
    entry.parameter_type = parameter_type
    entry.activate = activate
    return entry