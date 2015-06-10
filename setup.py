from setuptools import setup, find_packages

setup(
    name='have-a-rest',
    version=".".join(map(str, __import__("have_a_rest").__version__)),
    description='Gracefully describe your api model and documenting',
    author='torpedoallen',
    author_email='torpedoallen@gmail.com',
    url='http://github.com/torpedoallen/have-a-rest',
    packages=find_packages(),
    classifiers=[
    ],
    license="MIT",
)
