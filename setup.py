from setuptools import setup, find_packages


try:
    with open("README.md", "r") as readme:
        long_description = readme.read()
except:
    long_description = "Library for searching answers to school questions."

setup(
    name="ruotvet",
    version="0.0.4.2",
    description="Library for searching answers to school questions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="answers znanija otvet.mail.ru yandex.com/q/ resheba",
    author="xcaq",
    author_email="swipduces@yandex.com",
    python_requires=">=3.6.0",
    url="https://github.com/ruotvet/ruotvet",
    packages=find_packages(),
    install_requires=["aiohttp", "beautifulsoup4", "pydantic"],
    include_package_data=True,
    license="GNU LGPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
    ]
)