import os

from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call


class InstallCommand(install):
    def run(self):
        install.run(self)
        check_call(["glib-compile-schemas", os.path.join(self.install_data, "share/glib-2.0/schemas/")])


setup(name='photometrics-viewer',
      version='0.2',
      description='Viewing tool for photometrics files',
      url='http://github.com/dlippok/photoetric-viewer',
      author='Damian Lippok',
      author_email='mail.dalee@gmail.com',
      license='MIT',
      packages=find_packages(),
      cmdclass={
          'install': InstallCommand,
      },
      entry_points={
          'console_scripts': ['photometrics-viewer=photometric_viewer.main:run'],
      },
      package_data={
          'photometric_viewer': ['styles/style.css'],
      },
      data_files=[
          ('share/icons/hicolor/scalable/apps', ['data/icons/io.github.dlippok.photometrics-viewer.svg']),
          ('share/icons/hicolor/symbolic/apps', ['data/icons/io.github.dlippok.photometrics-viewer-symbolic.svg']),
          ('share/applications', ['data/desktop/io.github.dlippok.photometrics-viewer.desktop']),
          ('share/mime/packages', ['data/desktop/io.github.dlippok.photometrics-viewer.mime.xml']),
          ('share/metainfo', ['data/io.github.dlippok.photometrics-viewer.metainfo.xml']),
          ('share/glib-2.0/schemas/', ['data/io.github.dlippok.photometrics-viewer.gschema.xml'])
      ],
      test_suite="tests",
      zip_safe=False)
