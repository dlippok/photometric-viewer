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
      package_data = {
            'photometric_viewer': ['styles/style.css'],
      },
      zip_safe=False)
