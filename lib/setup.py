from os.path import isfile
from setuptools import setup, find_packages
from platform import system

SCRIPTS = []
if "Windows" == system():
    SCRIPTS = ["ubuild.bat", "ubuild.py"]
if "Linux" == system():
    SCRIPTS = ["ubuild"]

setup(
    name = "ubuild",
    version = "0.1.1",
    author = "Jeff Rimko",
    author_email = "jeffrimko@gmail.com",
    description = "A no-frills build script framework.",
    license = "MIT",
    keywords = "cli menu",
    url = "https://github.com/jeffrimko/Ubuild",
    py_modules=["ubuild"],
    scripts=SCRIPTS,
    long_description=open("README.rst").read() if isfile("README.rst") else "",
    install_requires=[
       "auxly>=0.5.2",
       "qprompt>=0.11.1"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ],
)
