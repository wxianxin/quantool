""""""


from setuptools import setup, find_packages


with open("README.md") as f:
    long_description = f.read()

with open("LICENSE") as f:
    license = f.read()

# exec(open("quantool/version.py").read())
with open("quantool/version.py") as f:
    __version__ = f.read()
setup(
    name="quantool",
    version=__version__,
    author="Steven Wang",
    description="Quant Tools for Financial Calculations",
    long_description=long_description,
    author_email="",
    url="https://github.com/wxianxin/quantool",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=["numpy", "scipy"],
    python_requires=">=3.6.0"
)
