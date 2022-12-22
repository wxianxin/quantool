""""""


from setuptools import setup, find_packages


with open("README.md") as f:
    long_description = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="quantool",
    setup_requires=["setuptools_scm"],
    use_scm_version=True,
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
