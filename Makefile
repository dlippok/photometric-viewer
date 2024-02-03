SOURCES = $(shell find photometric_viewer/ -name "*.py")
POS = $(shell find data/translations/ -name "*.po")

all: $(POS) test

.PHONY: test run clean flatpak-install flatpak-build flatpak-run flatpak-uninstall build

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

build:
	mkdir -p build
	glib-compile-schemas data/ --targetdir=build

	mkdir -p build/translations/de/LC_MESSAGES/
	msgfmt data/translations/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.po \
  		-o build/translations/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.mo

	mkdir -p build/translations/pl/LC_MESSAGES/
	msgfmt data/translations/pl/LC_MESSAGES/io.github.dlippok.photometric-viewer.po \
		-o build/translations/pl/LC_MESSAGES/io.github.dlippok.photometric-viewer.mo

install: build
	pip3 install .

# Flatpak
flatpak-build: build
	flatpak-builder --force-clean build/flatpak flatpak.yaml

flatpak-install: build
	flatpak-builder --user --install --force-clean build/flatpak flatpak.yaml

flatpak-run: flatpak-install
	flatpak run io.github.dlippok.photometric-viewer

flatpak-uninstall:
	flatpak uninstall -y io.github.dlippok.photometric-viewer

# Other
test:
	python3 -m "unittest" discover --start-directory tests/ -p "*.py"

clean:
	rm -rf .flatpak-builder
	rm -rf build


run: test build
	python3 run.py