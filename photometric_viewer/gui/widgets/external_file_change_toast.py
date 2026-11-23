from gi.repository import Adw


class ExternalFileChangeToast:
    def __init__(self, overlay: Adw.ToastOverlay, on_undo):
        self.overlay = overlay
        self.on_undo = on_undo
        self.toast: Adw.Toast | None = None

    def show(self):
        self.dismiss()

        toast = Adw.Toast.new(_("The photometric file has been modified on the disk"))
        toast.set_button_label(_("Undo"))
        toast.set_timeout(5)
        toast.connect("button-clicked", self.on_toast_undo)
        toast.connect("dismissed", self.on_toast_dismissed)
        self.toast = toast
        self.overlay.add_toast(toast)

    def on_toast_undo(self, *args):
        self.on_undo()
        self.dismiss()

    def on_toast_dismissed(self, toast: Adw.Toast):
        if self.toast is toast:
            self.toast = None

    def dismiss(self):
        toast = self.toast
        self.toast = None
        if toast:
            toast.dismiss()
