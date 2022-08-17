import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="schema-validator",
    version="0.0.0",
    author="Ram Kumar",
    description="Validate python dictionaries (mongodb docs etc) using a JSON schema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ramkrram/Schema_validator_script",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)