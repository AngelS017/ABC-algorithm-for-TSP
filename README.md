<h1 align="center"> ABC for TSP </h1>

<p align="center"> 
  <img src="images/presentation/ABC_logo.jpg" alt="ABC Logo">
</p>

<h3 align="center"> Real case of Artificial Bee Colony in a Travel Salesman Problem, a comparative study of different techniques for the generation of new solutions</h3>


## :book: Table of Contents

<details open="open">
  <summary>Table of Contents</summary>

1. [➤ About The Project](#about-the-project)
2. [➤ Prerequisites](#prerequisites)
3. [➤ Installation](#installation)
4. [➤ Folder Structure](#folder-structure)
5. [➤ Dataset](#dataset)
6. [➤ Test Environment](#test-environment)
7. [➤ Results and Discussion](#results-and-discussion)
8. [➤ References](#references)

</details>


## :memo: About The Project <a id="about-the-project"></a>

## :wrench: Prerequisites <a id="prerequisites"></a>

The following open source packages are used to develop this project:
* numpy
* matplotlib
* pandas
* scipy
* tqdm
* joblib


Furthermore, the environment utilized for the development of the ABC algorithm for the TSP can be used directly for your purposes.

The anaconda environment can be created as follows:

    conda env create -f ABC_for_TSP.yml

## :gear: Installation <a id="installation"></a>

Once all the prerequisites packages have been installed, the package for the algorithm Artificial Bee Colony can be installed for use in solving the Travel Salesman Problem.

    pip install abc-tsp


## :file_folder: Folder Structure <a id="folder-structure"></a>

    ABC-ALGORITHM-FOR-TSP
    ├── ABC_algorithm_TSP.ipynb
    ├── ABC_for_TSP.yml
    ├── LICENSE
    ├── README.md
    │   
    ├── ArtificialBeeColony_TSP
    |   ├── abc_tsp
    |   |   ├── ArtificialBeeColony_TSP.py
    |   |   └── __init__.py
    |   ├── README.md
    |   ├── LICENSE
    |   └── setup.py
    │   
    │   
    ├── data
    │   └── lu980.tsp
    │   
    ├── images
    │   ├── presentation
    │   │   └── ABC_logo.jpg
    │   └── project_analysis
    │       ├── limit_correction.png
    │       ├── Limit_correction_comparison.png
    │       ├── normal_training.png
    │       └── normal_training_comparison.png


## :books: Dataset <a id="dataset"></a>

The data that we are going to use in this proyect will be obtein from a web call [National TSP](https://www.math.uwaterloo.ca/tsp/world/countries.html) from the University of Waterloo.

This website was created to collect large-scale data on the Travel Seller Problem from different countries. In each country you can find a different number of cities which are represented with their X and Y coordinates. The **cost of traveling between cities is specified by the Euclidean distance** rounded to the nearest whole number.

<br>

In this case we are going to work with the dataset of the country [Luxembourg](https://www.math.uwaterloo.ca/tsp/world/lu980.tsp), which conteins 980 cities but there are some cities duplicated, following the removal of the duplicate cities, a total of 634 remain.

The following example illustrates the structure of the dataset:

```
      Coord X	 Coord Y
1	49525.5556	5940.5556
2	49525.5556	5940.5556
3	49738.8889	6345.0000
4	49608.3333	6405.8333
5	49796.6667	6155.5556
...	  ...	       ...
```

<br>

The website provides information on the optimal solution, among other things:
* **Optimal value (min path distance):** 11340
* **Algorithm:** concorde (default settings), QSopt LP solver
* **Time:** 1681.68 seconds, AMD Athlon 1.33 GHz


## :computer: Test Environment <a id="test-environment"></a>

The testing and algorithm development were conducted in a controlled environment with the following hardware and software configuration:

* Processor (CPU): Intel Core i9-14900HX up to 5.8 GHz Max Turbo (24 cores, 32 threads)
* Memory (RAM): 32 GB DDR5 at 5600 MHz
* Graphics Card (GPU): NVIDIA GeForce RTX 3080 Ti with 12 GB VRAM
* Operating System: Windows 11 (64-bit)
* Python Version: 3.12.4
* Key Libraries and Dependencies:

  * numpy 2.0.1
  * matplotlib 3.9.1
  * pandas 2.2.2
  * tqdm 4.66.5
  * scipy 1.14.0


Benchmark results and time analyses are included in the Results section of this repository.


## :mag_right: Results and Discussion <a id="results-and-discussion"></a>

## :link: References <a id="references"></a>