from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="abc_tsp",
    version="2.0.1",
    license='MIT',
    author="Angel Sanz Gutierrez",
    author_email="sanzangel017@gmail.com",
    description="Artificial Bee Colony TSP solver",
    keywords = ['Artificial Bee Colony', 'ABC', 'Optimizer', 'TSP', 'k-opt', 'metaheuristic'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AngelS017/ABC-algorithm-for-TSP",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'numpy>=1.20',
        'tqdm',
        'joblib',
    ],
    python_requires='>=3.8'
)
