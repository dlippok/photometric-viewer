build:
	python3 setup.py build

run:
	python3 run.py

flatpak-build: flatpak.yaml
	flatpak-builder --force-clean build/flatpak flatpak.yaml

flatpak-install: flatpak-build
	flatpak-builder --user --install --force-clean build/flatpak flatpak.yaml

flatpak-run: flatpak-install
	flatpak run io.github.dlippok.photometric-viewer

flatpack-uninstall:
	flatpak uninstall -y io.github.dlippok.photometric-viewer

flatpak-clean:
	rm -rf build/flatpak


clean: flatpak-clean
	rm -rf build