# Nature Inspired Optimisation Algorithms on the Brachistochrone problem

This project is an offshoot inspired by (but separate to) my Extended Project Qualification "To what extent does an inspiration from Nature result in the creation of an effective Optimisation Algorithm?"

The code BrachistochroneVisualise.py when executed prompts the user which algorithm they would like to use, after which a pygame GUI shows the algorithm iteratively solving the Brachistochrone problem, N = 25, for 500 iterations:

![Example Test run](/Brachistochrone/examplerun.png)

### Prerequisites

The code was programmed in Python 3.8.0, and uses the external libraries: NumPy, SciPy, Pygame and cma. Once Python is installed, the following script in Adminstrator Command Prompt will download the relevant libraries:

```
pip install numpy, scipy, pygame, cma
```

## The Brachistochrone Problem

The Brachistochrone Problem, posed by Bernouilli in 1696, essentially asks the question "What is the shape of the curve in which a mass slides from point A to point B in the least time?" A helpful animation on Wikipedia illustrates the solution to this problem:

![Brachistochrone](/Brachistochrone/Brachistochrone.gif)

This curve can be approximated using a piecewise slope composed of N line segments, and thus the time for a mass to slide down this discrete slope can be calculated (assuming instantaneous change of velocity at each vertex).

The algorithms optimise a function that takes in a N-dimensional vector containing the y-coordinates of the line segments that define each slope, and outputs the resulting time to slide down.

## Algorithms

I attach a in-depth review of my implementations of these algorithms and how they work, itself an excerpt from my EPQ dissertation that discusses their applications in my main project, involving the benchmarking of these algorithms. Note that the implementation described in the document has been adapted for use to this specific problem, but the vast majority of information is applicable.

[Algorithms Document](https://github.com/raahweng/Nature-Inspired-Optimisation/blob/master/Brachistochrone/Algorithms.docx)

