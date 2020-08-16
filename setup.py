import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paradboxes",
    version="0.0.1",
    author="Nathan Turner",
    author_email="nathanturner270@gmail.com",
    description="Manipulate paradboxes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NathanTurner270/paradboxes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
