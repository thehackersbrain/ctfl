from setuptools import setup, find_packages
from ctfl import __version__


with open("README.md") as readme:
    long_description = readme.read().strip()


setup(
    name="ctfl",
    version=__version__,
    description="CTFTime Upcoming CTF Lists",
    author="Gaurav Raj",
    url="https://github.com/thehackersbrain/ctfl",
    author_email="techw803@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["ctf", "ctftime", "thehackersbrain", "gauravraj", "python"],
    packages=find_packages(),
    install_requires=["rich", "requests", "bs4"],
    entry_points={"console_scripts": ["ctfl=ctfl.__main__:main"]},
    zip_safe=False,
)
