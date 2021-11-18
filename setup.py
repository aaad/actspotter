import io
import os

import setuptools


# Package metadata.

name = "actspotter"
description = "Actspotter library for detecting activities"
version = "0.1.2"
release_status = "Development Status :: 4 - Beta"
dependencies = [
    "tensorflow >= 2.6.0",
]
extras = {}


# Setup boilerplate below this line.

package_root = os.path.abspath(os.path.dirname(__file__))
readme_filename = os.path.join(package_root, "README.rst")
with io.open(readme_filename, encoding="utf-8") as readme_file:
    readme = readme_file.read()

# Only include packages under the 'google' namespace. Do not include tests,
# benchmarks, etc.
packages = [
    package for package in setuptools.find_packages()
]

setuptools.setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    author="Simon Hecht",
    author_email="simon_hecht@hotmail.com",
    license="GPL 3.0",
    url="https://github.com/aaad/actspotter",
    classifiers=[
        release_status,
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    platforms="Posix; MacOS X; Windows",
    packages=packages,
    install_requires=dependencies,
    extras_require=extras,
    python_requires=">=3.6",
    scripts=[],
    include_package_data=True,
    zip_safe=False,
)
