.PHONY = test run clean flatpak-install flatpak-build flatpak-run flatpak-uninstall
SOURCES = $(shell find photometric_viewer/ -name "*.py")
POS = $(shell find data/translations/ -name "*.po")

all: $(POS) test

# Translations
data/translations/io.github.dlippok.photometric-viewer.pot: $(SOURCES)
	xgettext $? data/translations/io.github.dlippok.photometric-viewer.pot \
		-o data/translations/io.github.dlippok.photometric-viewer.pot


data/translations/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.po: data/translations/io.github.dlippok.photometric-viewer.pot
	msgmerge \
  		data/translations/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.po \
  		data/translations/io.github.dlippok.photometric-viewer.pot \
		-o data/translations/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.po

data/translations/pl/LC_MESSAGES/io.github.dlippok.photometric-viewer.po: data/translations/io.github.dlippok.photometric-viewer.pot
	msgmerge \
  		data/translations/pl/LC_MESSAGES/io.github.dlippok.photometric-viewer.po \
  		data/translations/io.github.dlippok.photometric-viewer.pot \
		-o data/translations/pl/LC_MESSAGES/io.github.dlippok.photometric-viewer.po

compile-translations: $(POS)
	msgfmt data/translations/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.po \
  		-o data/translations/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.mo
	msgfmt data/translations/pl/LC_MESSAGES/io.github.dlippok.photometric-viewer.po \
		-o data/translations/pl/LC_MESSAGES/io.github.dlippok.photometric-viewer.mo

# Flatpak
flatpak-build:
	flatpak-builder --force-clean build/flatpak flatpak.yaml

flatpak-install: test
	flatpak-builder --user --install --force-clean build/flatpak flatpak.yaml

flatpak-run: flatpak-install
	flatpak run io.github.dlippok.photometric-viewer

flatpak-uninstall:
	flatpak uninstall -y io.github.dlippok.photometric-viewer

# Other
test:
	python3 setup.py test

clean:
	find data/translations/ -name "*.mo" -delete
	rm -rf .flatpak-builder
	rm -rf build


run: test compile-translations
	python3 run.py