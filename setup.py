from setuptools import setup, find_packages

setup(name='photometric-viewer',
      version='2.1.2',
      description='Browse content of IES and LDT photometric files',
      url='https://github.com/dlippok/photometric-viewer',
      project_urls={
            "Bug Tracker": 'https://github.com/dlippok/photometric-viewer/issues',
            "Support": 'https://github.com/dlippok/photometric-viewer/discussions/categories/q-a'
      },
      author='Damian Lippok',
      author_email='mail.dalee@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['photometric-viewer=photometric_viewer.main:run'],
      },
      package_data={
          'photometric_viewer': [
              'assets/style.css',
              'assets/language-specs/ies.lang',
              'assets/language-specs/ldt.lang',
          ],
      },
      data_files=[
          ('share/icons/hicolor/scalable/apps', ['data/icons/io.github.dlippok.photometric-viewer.svg']),
          ('share/icons/hicolor/symbolic/apps', ['data/icons/io.github.dlippok.photometric-viewer-symbolic.svg']),
          ('share/locale/de/LC_MESSAGES', ['build/translations/de/LC_MESSAGES/io.github.dlippok.photometric-viewer.mo']),
          ('share/locale/pl/LC_MESSAGES', ['build/translations/pl/LC_MESSAGES/io.github.dlippok.photometric-viewer.mo']),
          ('share/icons/hicolor/symbolic/apps', ['data/icons/io.github.dlippok.photometric-viewer-symbolic.svg']),
          ('share/applications', ['data/desktop/io.github.dlippok.photometric-viewer.desktop']),
          ('share/mime/packages', ['data/desktop/io.github.dlippok.photometric-viewer.mime.xml']),
          ('share/metainfo', ['data/io.github.dlippok.photometric-viewer.metainfo.xml']),
          ('share/glib-2.0/schemas', ['data/io.github.dlippok.photometric-viewer.gschema.xml', 'build/gschemas.compiled'])
      ],
      test_suite="tests",
      zip_safe=False)
