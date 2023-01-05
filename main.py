#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
'''An example of how to use the `Fridge` class.

Do note that multiprocessing is using the `map` function.
If instead we only want to store the result for further
processing as a `pickle`, then `imap_unordered` can be
used instead because significantly faster.

After 1000 simulations with the smart thermostat, the 
result should be something like 9.139,46 DKK. With the 
normal thermostat is should be 13.947,61 DKK.

'''

from fridge import Fridge
from multiprocessing import Pool
from numpy import average
from time import time

M: int = 10  # number of simulations


def call(*args):
    return Fridge(SMART=True).simulate()


def main():
    with Pool() as p:
        return average(p.map(call, range(M)))


if __name__ == "__main__":
    START_TIME = time()
    print(main())
    print(time()-START_TIME)
