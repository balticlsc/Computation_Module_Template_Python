import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="balticlsc_test",
    version="0.1.0",
    author="BalticLSC",
    author_email="Kamil.Rybinski@pw.edu.pl",
    description="Baltic LSC module old_scheme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/balticlsc/Computation_Module_Template_Python",
    install_requires=[
        'flask',
        'requests',
        'pymongo'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
