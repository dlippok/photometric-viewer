from setuptools import setup, find_packages

setup(name='photometric-viewer',
      version='2.1.2',
      description='Browse content of IES and LDT photometric files',
      url='https://github.com/dlippok/photometric-viewer',
      project_urls={
            "Issues": 'https://github.com/dlippok/photometric-viewer/issues',
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
      zip_safe=False)
