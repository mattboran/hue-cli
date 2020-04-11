import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

# tests_require = ['pytest', 'pytest-cov']
tests_require = []

setuptools.setup(
    name="hue_cli",
    version="0.1.0",
    author="Matt Boran",
    author_email="mattboran@gmail.com",
    description="CLI forr Philips Hue bulbs",
    long_description="To come",
    long_description_content_type="text/markdown",
    url="https://github.com/mattboran/hue-cli",
    download_url="https://github.com/mattboran/hue-cli/releases/download/0.1.0/hue_cli-0.1.0-py3-none-any.whl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'hue_py'
    ],
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
    extras_require={
        'test': tests_require
    },
    python_requires='>3.6.0',
    entry_points={
        'console_scripts': [
            'hue = hue_cli.cli:run'
        ]
    }
)
