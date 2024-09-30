from distutils.core import setup

setup(
    name="pyflorist",  # How you named your package folder (MyLib)
    packages=["pyflorist"],  # Chose the same as "name"
    version="0.1",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="A Python client for the Florist One API, enabling easy flower delivery integration.",  # Expanded description
    long_description=open(
        "README.md"
    ).read(),  # Long description pulled from the README file
    long_description_content_type="text/markdown",  # Give a short description about your library
    author="reed jones",  # Type in your name
    author_email="reedmjones@outlook.com",  # Type in your E-Mail
    url="https://github.com/reedjones/pyflorist",  # Provide either the link to your github or to your website
    download_url="https://github.com/reedjones/pyflorist/archive/v_01.tar.gz",  # I explain this later on
    keywords=[
        "florist",
        "flower delivery",
        "API client",
        "e-commerce",
        "online shopping",
        "checkout integration",
    ],  # Keywords for searching
    install_requires=[  # I get to this in a second
        "requests",
        "pydantic",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3",  # Specify which pyhton versions that you want to support
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    project_urls={  # Additional URLs related to the project
        "Documentation": "https://github.com/reedjones/pyflorist#readme",
        "Source": "https://github.com/reedjones/pyflorist",
        "Tracker": "https://github.com/reedjones/pyflorist/issues",
    },
)
