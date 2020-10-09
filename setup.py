from setuptools import setup

setup(name='plaza-matrix-service',
      version='0.1',
      description='Plaza service to use Matrix.im bots.',
      author='kenkeiras',
      author_email='kenkeiras@codigoparallevar.com',
      license='Apache License 2.0',
      packages=['plaza_matrix_service'],
      scripts=['bin/plaza-matrix-service'],
      include_package_data=True,
      install_requires=[
          'matrix_client',
          'programaker_bridge',
          'xdg',
      ],
      zip_safe=False)
