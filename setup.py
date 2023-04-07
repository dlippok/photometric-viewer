from setuptools import setup, find_packages

setup(name='photometric-viewer',
      version='0.1',
      description='Viewing tool for photometric files',
      url='http://github.com/dlippok/photoetric-viewer',
      author='Damian Lippok',
      author_email='mail.dalee@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points={
        'console_scripts': ['photometric-viewer=photometric_viewer.main:run'],
      },
      package_data={
            'photometric_viewer': ['styles/style.css'],
      },
      data_files=[
            ('share/icons/hicolor/scalable/apps', ['data/icons/info.dalee.photometric-viewer.svg']),
            ('share/icons/hicolor/symbolic/apps', ['data/icons/info.dalee.photometric-viewer-symbolic.svg']),
            ('share/applications', ['data/desktop/info.dalee.photometric-viewer.desktop']),
            ('share/mime/packages', ['data/desktop/info.dalee.photometric-viewer.mime.xml']),
            ('share/metainfo/', ['info.dalee.photometric-viewer.metainfo.xml'])
      ],
      zip_safe=False)
