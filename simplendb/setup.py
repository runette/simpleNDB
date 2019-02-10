import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="simplendb",
    version= "0.9.1",
    author="Paul Harwood",
    author_email="runette@gmail.com",
    description="A very simple package to mnake Google Cloud Clients look more like appengine.api and NDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/runette/simpleNDB",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python ::3",
        "License :: OSI Approved :: MIT Licence",
        "Operating System :: OS Independent",
        "Development Status :: Beta",
    ]
)