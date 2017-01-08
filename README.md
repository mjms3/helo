# Euclidean Shortest Path (ESP)

## Introduction

This repository contains some simple code for solving a version of
the Euclidean Shortest Path problem. The Euclidean Shortest Path
problem consists of finding a shortest path through a piecewise Euclidean
space. That is, the space is divided into a finite number of regions
in each of which the metric is locally Euclidean.

A survey of this problem is described in [Geometric Shortest Paths and
Network Optimisation](www.ams.sunysb.edu/~jsbm/papers/survey.ps.gz) by Joseph
Mitchell. The approach adopted here is similar to the Pathnet method described on
page 13 of the review. This approach involves constructing a discretised version of
the problem as a graph and then applying Dijkstra's algorithm. In practice, this approach
is considerably more computationally intensive than necessary (especially given
the way it is implemented here, where the emphasis was on getting something that works
as quickly as possible by leveraging pre-existing library code).

However, the approach defined here does work well for even moderately complex problems
and provides a good basis for solving the problem in a more efficient way.

## Getting Up and Running

The code is written in Python 3, and makes heavy use of matplotlib. The file `environment.yml`
contains a list of all packages and versions that are used. This is designed to recreate
a python virtual environment using [anaconda](https://www.continuum.io/downloads). Once the
`conda` package manager is installed, it should be possible to recreate the environment using
`conda env create -f environment.yml`. Note that anaconda was used rather than the more
standard virtual env as some of the (mainly C based) dependencies of matplotlib do not
work well with a standard python virtual env.

There is a series of unit tests in esp/tests. These tests can be run with a standard python
unittest runner such as nose.

## Commentary on the Code

The unittests (especially for esp.py) show the expected use of the ShortestPathFinder class.
Putting together the code has suggested that the best way to think about the problem is in
two parts:

* An underlying representation of known speed penalties. This should be in terms of
a triangulation of the problem domain with associated weights.
* A method to find the shortest path that takes, at a bare minimum, the start and end points
in the domain.

The way the calculation is currently carried out is not particularly efficient, in particular,
it involves multiple calculations of the same data and the underlying triangulation is
not stored in a way that is particularly appropriate for the problem of interest. The algorithm
used, whilst in no way a "brute force" algorithm is, neverthless, not optimal in either
time or space. However, optimising it in its current form does not seem sensible, for reasons
discussed in the Next Steps section below.

### Interface

In the short term, it seems like a good way to make use of the code is by calling it directly
from whatever framework is being used for the web code. Depending on the language / framework
being used, there may be some better ways to do this. One possibility is to modify the code to
use [bokeh](http://bokeh.pydata.org/en/latest/). In which case, the final output would be
a json object suitable for rendering by bokeh.js.


## Next Steps

As this code is very much meant to be a PoC, there doesn't seem to be much point in optimising
the existing code (although there are plenty of ways in which this is possible). My proposed next steps
on the path finding front would be something along the lines of:

* Prototype a better algorithm that takes into account known geometric properties of
the problem in a sensible way. This would probably be based on [bushwack](https://users.cs.duke.edu/~reif/paper/sunz/bushwhack/bushwhack.ps)
and could be done in python. The current unit tests in test_esp.py are agnostic to the
algorithm used for finding the shortest path so should provide a good safety net.
* Reimplement the prototyped algorithm in C++. It would also be worthwhile implementing
(or finding suitable library code) for a different triangulation storage methodology as
the one that we're currently using is not appropriate. This provides a mechanism to
quickly calculate the shortest paths in real time.
* In the meantime, it is important to get accurate data for the underlying speed penalties
by region.
