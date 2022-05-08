from setuptools import find_packages, setup
setup(
    name='gdbPy',
    packages=find_packages(include=['gdbPy']),
    version='0.1.0',
    description='gdb scripts in Python',
    author='Marco Balossini',
    license='GPL',
    url="https://github.com/MarcoBalossini/gdbPy",
    keywords=["gdb", "debugging"],
    classifiers=[
    'Intended Audience :: Developers',
    'License :: GPL License',
    'Programming Language :: Python :: 3',
  ],
)