import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Net2Scripting",
    version="5.0.0",
    author="Cor Kalis",
    author_email="info@net2scripting.nl",
    description="Python scripting for Paxton Net2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cor-kalis/Net2Scripting",
    packages=setuptools.find_packages(),
    install_requires=[
        'pythonnet'
    ],
    package_data={
        '': ['libs/log4netdll/*.dll', 
             'libs/paxton/*.dll',
             'Net2Scripting.config'
         ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    )
)
