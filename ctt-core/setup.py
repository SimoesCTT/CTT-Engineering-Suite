from setuptools import setup, find_packages

setup(
    name="ctt-core",
    version="1.0.0",
    author="Americo Simoes",
    author_email="amexsimoes@gmail.com",
    description="CTT Temporal Integration Engine",
    packages=find_packages(),
    install_requires=["numpy>=1.21.0"],
    license="Proprietary",
)
