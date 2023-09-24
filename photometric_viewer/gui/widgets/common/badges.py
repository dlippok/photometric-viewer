from gi.repository.Gtk import Image

def calculated():
    tooltip = _("Value was calculated from other properties and may not be accurate. "
                "Please refer to manufacturer's data sheet if available.")
    image = Image.new_from_icon_name("info-symbolic")
    image.set_tooltip_text(tooltip)
    return image
