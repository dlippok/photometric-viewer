# Test coverage limitations

The automated suite is run with `make test`, which uses Python `unittest` discovery under `tests/`. Existing tests cover photometric calculations and utilities, file I/O and formats, and IES/LDT parsing, conversion, extraction, and validation.

There are no tests for the GTK/Adwaita UI or its integration with Gio. In particular, passing `make test` does not verify widget behavior, window activation and timeout handling, metadata polling, or external file changes through Flatpak's document portal.

Changes to those areas require manual validation in the application. For external-file monitoring, include a Flatpak run and an edit/save from another application; the automated suite is not a substitute for that check.

# Application sandboxing

The Flatpak manifest uses the GNOME 50 runtime and grants IPC, Wayland/fallback X11, and DRI access. It does not grant broad host-filesystem access. The app uses `Gtk.FileChooserNative`, which in a Flatpak session normally goes through the desktop file chooser portal; selected files are made available through the document portal.

Consequences for file handling and tests:

- A selected file may have a portal path such as `/run/user/<uid>/doc/<id>/...`, not its original host path. Use the `Gio.File` returned by the chooser; do not assume paths are stable, canonical host paths or accessible outside the portal grant.
- Portal-mediated access and sandbox boundaries can affect filesystem monitoring. In the observed Flatpak setup, `Gio.FileMonitor` reported Photometric Viewer's own writes but did not report edits made by another Flatpak. The app therefore uses modification-time polling only (once per second while active), rather than combining it with `Gio.FileMonitor`.
- Flatpak behavior should be tested using files selected through the chooser and edits made by another application. Host-only tests do not exercise document-portal permissions or event delivery.

The Snap package is also confined (`strict`) and declares `home` and `removable-media` plugs. File-access behavior may therefore differ by package format and granted permissions; validate the relevant package separately.
