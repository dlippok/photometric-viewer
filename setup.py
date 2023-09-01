import os
from pathlib import Path
import shutil

from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call


class InstallCommand(install):
    def run(self):
        install.run(self)
        check_call(["glib-compile-schemas", os.path.join(self.install_data, "share/glib-2.0/schemas/")])

        translation_dirs = [p for p in Path("data/translations").iterdir() if p.is_dir()]
        for translation_dir in translation_dirs:
            lang = translation_dir.name
            check_call([
                "msgfmt",
                str(translation_dir / "LC_MESSAGES" / "io.github.dlippok.photometric-viewer.po"),
                "-o", str(translation_dir / "LC_MESSAGES" / "io.github.dlippok.photometric-viewer.mo")
            ])
            os.makedirs(os.path.join(self.install_data, f"share/locale/{lang}/LC_MESSAGES"), exist_ok=True)
            shutil.copy2(
                (translation_dir / "LC_MESSAGES" / "io.github.dlippok.photometric-viewer.mo"),
                os.path.join(self.install_data, f"share/locale/{lang}/LC_MESSAGES")
            )

setup(name='photometric-viewer',
      version='1.4.0',
      description='Browse content of IES and LDT photometric files',
      url='http://github.com/dlippok/photoetric-viewer',
      author='Damian Lippok',
      author_email='mail.dalee@gmail.com',
      license='MIT',
      packages=find_packages(),
      cmdclass={
          'install': InstallCommand,
      },
      entry_points={
          'console_scripts': ['photometric-viewer=photometric_viewer.main:run'],
      },
      package_data={
          'photometric_viewer': ['styles/style.css'],
      },
      data_files=[
          ('share/icons/hicolor/scalable/apps', ['data/icons/io.github.dlippok.photometric-viewer.svg']),
          ('share/icons/hicolor/symbolic/apps', ['data/icons/io.github.dlippok.photometric-viewer-symbolic.svg']),
          ('share/applications', ['data/desktop/io.github.dlippok.photometric-viewer.desktop']),
          ('share/mime/packages', ['data/desktop/io.github.dlippok.photometric-viewer.mime.xml']),
          ('share/metainfo', ['data/io.github.dlippok.photometric-viewer.metainfo.xml']),
          ('share/glib-2.0/schemas/', ['data/io.github.dlippok.photometric-viewer.gschema.xml'])
      ],
      test_suite="tests",
      zip_safe=False)
