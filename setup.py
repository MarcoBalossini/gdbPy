from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='gdbPy',
    packages=find_packages(include=['gdbPy']),
    version='0.1.2',
    description='gdb scripts in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Marco Balossini',
    license='GPL',
    url="https://github.com/MarcoBalossini/gdbPy",
    keywords=["gdb", "debugging"],
    classifiers= [
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Programming Language :: Python :: 3',
    ],
)