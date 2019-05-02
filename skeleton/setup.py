try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='gothonweb',
    version='1.0',
    description='Simple text-based game run in the web browser.',
    author='Mateusz Kanabrocki',
    author_email='mateusz.kanabrocki@gmail.com',
    packages=['gothonweb'],  #same as name
    install_requires=['nose'], #external packages as dependencies
    # 'py_modules': ['MODULE_NAME'],
    # 'scripts': [],
)

# config = {
#     'description': 'Simple text-based game run in the web browser.,
#     'author': 'Mateusz Kanabrocki',
#     # 'url': 'https://github.com/mateuszkanabrocki/projects/tree/master/gothonweb',
#     'download_url': 'https://github.com/mateuszkanabrocki/projects/tree/master/gothonweb',
#     'author_email': 'mateusz.kanabrocki@gmail.com',
#     'version': '0.1',
#     'install_requires': ['nose'],
#     # 'packages': ['NAME'],
#     # 'py_modules': ['MODULE_NAME'],
#     # 'scripts': [],
#     'name': 'projectnamegothonweb'

# setup(**config)
