echo -n "Updating template from sources ... "
xgettext \
  $(find photometric_viewer/ -name "*.py" | xargs) \
  data/translations/io.github.dlippok.photometric-viewer.pot \
  -o data/translations/io.github.dlippok.photometric-viewer.pot
echo "done."

echo -n "Updating DE "
msgmerge \
  data/translations/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.po \
  data/translations/io.github.dlippok.photometric-viewer.pot \
  -o data/translations/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.po

