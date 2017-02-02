python-moos tutorials
=====================

A bunch of easy to understand/use [MOOS][] examples through python.

## Installation

To launch the examples, you need:
1. [`core-moos`][0] (where MOOSDB and libmoos live),
2. [`essential-moos`][2] (to use `pAntler` and `pShare`), and
3. [`python-moos`][1] (for the `pymoos` python package).

In a terminal:

### 1. `core-moos`
```shell
git clone https://github.com/themoos/core-moos
cd core-moos
mkdir build
cd build
cmake ..
make
sudo make install
cd ../..
```

### 2. `essential-moos`
```shell
git clone https://github.com/themoos/essential-moos
cd essential-moos
mkdir build
cd build
cmake ..
make
sudo make install
cd ../..
```


### 3. `python-moos`
```shell
git clone https://github.com/msis/python-moos
cd python-moos
mkdir build
cd build
cmake ../
make
sudo make install
cd ../..
```

## Usage

Once you have `pymoos` package installed, you can then try and play with any of the examples in the subfolders.

[MOOS]: http://themoos.org
[0]:    https://github.com/themoos/core-moos
[2]:    https://github.com/themoos/essential-moos
[1]:    https://github.com/msis/python-moos
