from setuptools import setup, find_packages
import pathlib
import re

WORK_DIR = pathlib.Path(__file__).parent

try:
    with open("README.md", "r", encoding="utf-8") as readme:
        long_description = readme.read()
except:
    long_description = "Library for searching answers to school questions."


def get_version():
    try:
        file = (WORK_DIR / "ruotvet" / "__init__.py").read_text("utf-8")
        return re.findall(r"^__version__ = \"([^\"]+)\"\r?$", file, re.M)[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")


setup(
    name="ruotvet",
    version=get_version(),
    description="Library for searching answers to school questions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="gdz brainly otvet.mail.ru thequestion resheba",
    author="Kirill Feschenko",
    author_email="swipduces@yandex.com",
    python_requires=">=3.7.0",
    url="https://github.com/rgit/ruotvet/",
    packages=find_packages(),
    install_requires=["aiohttp", "aiofiles", "beautifulsoup4", "pydantic", "opencv-python", "pytesseract"],
    include_package_data=True,
    license="GNU LGPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Utilities",
        "Topic :: Education",
        "Typing :: Typed"
    ]
)
