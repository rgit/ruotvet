from setuptools import setup, find_packages


try:
    with open("README.md", "r") as readme:
        long_description = readme.read()
except:
    long_description = "Library for searching answers to school questions."

setup(
    name="old-ruotvet",
    version="0.0.1",
    description="Library for searching answers to school questions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="xcaq",
    author_email="swipduces@yandex.com",
    python_requires=">=3.6.0",
    url="https://github.com/ruotvet/ruotvet",
    packages=find_packages(),
    install_requires=["aiohttp", "beautifulsoup4", "opencv-python", "easyocr", "numpy", "pydantic"],
    include_package_data=True,
    license="GNU LGPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU LGPLv3 License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6+",
    ]
)