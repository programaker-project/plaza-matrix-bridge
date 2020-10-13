from setuptools import setup

setup(name='programaker-matrix-service',
      version='0.1',
      description='Programaker service to use Matrix.im bots.',
      author='kenkeiras',
      author_email='kenkeiras@codigoparallevar.com',
      license='Apache License 2.0',
      packages=['programaker_matrix_service'],
      scripts=['bin/programaker-matrix-service'],
      include_package_data=True,
      install_requires=[
          'matrix_client',
          'programaker_bridge',
          'xdg',
      ],
      zip_safe=False)
