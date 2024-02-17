SOURCES = $(shell find photometric_viewer/ -name "*.py")
POS = $(shell find data/translations/ -name "*.po")

build:
	mkdir -p build/dist/share/icons/hicolor/scalable/apps
	cp data/icons/io.github.dlippok.photometric-viewer.svg build/dist/share/icons/hicolor/scalable/apps

	mkdir -p build/dist/share/icons/hicolor/symbolic/apps
	cp data/icons/io.github.dlippok.photometric-viewer-symbolic.svg build/dist/share/icons/hicolor/symbolic/apps

	mkdir -p build/dist/share/applications
	cp data/desktop/io.github.dlippok.photometric-viewer.desktop build/dist/share/applications

	mkdir -p build/dist/share/mime/packages
	cp data/desktop/io.github.dlippok.photometric-viewer.mime.xml build/dist/share/mime/packages

	mkdir -p build/dist/share/metainfo
	cp data/io.github.dlippok.photometric-viewer.metainfo.xml build/dist/share/metainfo

	mkdir -p build/dist/share/glib-2.0/schemas
	cp data/io.github.dlippok.photometric-viewer.gschema.xml build/dist/share/glib-2.0/schemas
	glib-compile-schemas data/ --targetdir=build/dist/share/glib-2.0/schemas

	mkdir -p build/dist/share/locale/de/LC_MESSAGES
	msgfmt data/translations/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.po \
  		-o build/dist/share/locale/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.mo

	mkdir -p build/dist/share/locale/pl/LC_MESSAGES
	msgfmt data/translations/pl/LC_MESSAGES/io.github.dlippok.photometric-viewer.po \
		-o build/dist/share/locale/pl/LC_MESSAGES/io.github.dlippok.photometric-viewer.mo

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

install-pip:
	pip3 install . --prefix $(INSTALL_TARGET)

install-dist:
	echo "Installing distribution files"
	cp --recursive build/dist/* $(INSTALL_TARGET)

install: build install-pip install-dist

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