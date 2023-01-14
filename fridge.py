#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
'''The fridge module.

This module contains a single class called `Fridge`. This class
has been made in such a way, that multiple instances of the fridge
share comment constants and variables such as the starting
temperature `T_START`. This has been done to allow multiprocessing 
to function correctly.

Do note that the class has to instantiated before simulating. This 
has been done to allow generality between the computed fridge 
objects for multiprocessing. 

'''

__AUTHOR__ = "Mikkel-Coder"
__DATA__ = "05/01/2023"
__LICENSE__ = "MIT"
__STATUS__ = "No longer in development"
__VERSION__ = "1.0.0"
__DOCFORMAT__ = "numpy"


from numpy import exp, random, array, append, delete, arange
from pandas import read_csv


class Fridge:
    """An object of the fridge.

    Parameters
    ----------
    T_START : int or float, optional
        The starting temperature of the fridge in celsius, by default 5
    T_ROOM : int or float, optional
        The temperature outside the fridge, by default 20
    T_COMPRESSOR : int or float, optional
        The strength of the compressor to cool in celsius, by default -5
    T_TARGET : int or float, optional
        The target for the dum thermostat in celsius, by default 5
    SMART : bool, optional
        Determines if the smart thermostat is used or not, by default False
    W_CONSUMPTION : int, optional
        Power consumption in kWh pr five minute interval, ny default 1

    Attributes
    ----------
    __N : int
        Maximum number of loops, by default 8640
    __DELTA_T : int
        Number of seconds in five minutes, by default 300
    __t : numpy.array
        An empty list to append the inside temperature of the fridge.
    __expense : numpy.array
        An empty list to append the expense of power consumption and food waste.
    __ELECTRICITY_PRICE : pandas.DataFrame
        Object for lookup of the current electricity price.
    __thermostat_smart_result : bool
        Result of function `__thermostat_smart()`. Used for optimization.
    
    Reference
    ----------
    [1] T. Kallehauge, M. V. Vejling, J. J. Nielsen (17 November, 200) Grundlæggende programmering Workshop II: Kølerum.
    
    Examples
    --------
    >>> y = Fridge()
    >>> y.simulate()
    13813.11500000001
    >>> x = Fridge(SMART=True)
    >>> x.simulate()
    8666.461844978892
    """
    __N: int = 8640
    __DELTA_T: int = 300
    __t: list = array([], dtype=float)
    __expense: list = array([], dtype=float)
    __ELECTRICITY_PRICE: object = read_csv('electricity_price.csv')
    __thermostat_smart_result: bool = None

    def __init__(self,
                 T_START: int or float = 5,
                 T_ROOM: int or float = 20, 
                 T_COMPRESSOR: int or float = -5, 
                 T_TARGET: int or float = 5, 
                 SMART: bool = False,
                 W_CONSUMPTION: int or float = 1) -> None:
        self.__T_START = T_START
        self.__T_ROOM = T_ROOM
        self.__T_COMPRESSOR = T_COMPRESSOR
        self.__T_TARGET = T_TARGET
        self.__SMART = SMART
        self.__W_CONSUMPTION = W_CONSUMPTION

    def __c_1(self) -> float:
        """Returns a float depending if the fridge was open or not.

        Returns
        -------
        float
            The frequency of temperature loss.
        
        Note
        ----
        You should not call this method. 
        
        References
        ----------
        [1] (T. Kallehauge, M. V. Vejling, J. J. Nielsen, 2022, pp 2-3)

        
        Examples
        --------
        >>> Fridge().__c_1()
        5e-07
        """
        if random.choice(a=[True, False], p=[0.1, 0.9]): 
            return 3*10**-5 
        else: 
            return 5*10**-7

    def __c_2(self) -> float:
        """Returns a float depending on what thermostat was in use.

        Returns
        -------
        float
            The frequency of temperature cooling.
        
        Note
        ----
        You should not call this method. 
        
        References
        ----------
        [1] (T. Kallehauge, M. V. Vejling, J. J. Nielsen, 2022, pp 2)
        
        Examples
        --------
        >>> Fridge().__c_2()
        0
        """
        match self.__SMART:
            case True: 
                if self.__thermostat_smart_result:
                    return 8*10**-6
                else:
                    return 0
            case False: 
                if self.__thermostat():
                    return 8*10**-6 
                else: 
                    return 0

    def __thermostat(self) -> bool:
        """Returns a bool if the compressor was on or off.
    
        This thermostat work by turing on the compressor if the temperature
        inside the fridge is greater than five degrees celsius. 

        Returns
        -------
        bool
            The compressor on or off.   
        
        Note
        ----
        You should not call this method. 
        
        References
        ----------
        [1] (T. Kallehauge, M. V. Vejling, J. J. Nielsen, 2022, pp 2)
        
        Examples
        --------
        >>> Fridge().__thermostat()
        False
        """
        if self.__t[self.__n-1] > self.__T_TARGET:
            return True
        else:
            return False

    def __thermostat_smart(self) -> bool:
        """Returns a bool if the compressor was on or off.

        This is the smart thermostat. It works by checking if it is cheaper
        to throw the food away than turning on the compressor.

        Returns
        -------
        bool
            `True` if it is cheaper to throw the food away.
            `False` if it is cheaper to run the compressor.
        
        Note
        ----
        You should not call this method. 
        
        Examples
        --------
        >>> Fridge().__thermostat_smart()
        False
        """
        if self.__food_expense() < self.__ELECTRICITY_PRICE.iat[self.__n, 1]:
            return True
        else:
            return False

    def __power_expense(self) -> float:
        """Returns the expense of running the compressor or not.

        Returns
        -------
        float
            Returns the expense of running the compressor or not.
        
        Note
        ----
        You should not call this method. 
        
        References
        ----------
        [1] (T. Kallehauge, M. V. Vejling, J. J. Nielsen, 2022, pp 3)
        
        Examples
        --------
        >>> Fridge().__power_expense()
        0
        """
        match self.__SMART:
            case True: 
                if self.__thermostat_smart_result:
                    return 0 
                else:
                    return self.__ELECTRICITY_PRICE.iat[self.__n, 1] * self.__W_CONSUMPTION
            case False: 
                if self.__thermostat():
                    return self.__ELECTRICITY_PRICE.iat[self.__n, 1] * self.__W_CONSUMPTION
                else:
                    return 0

    def __food_expense(self) -> float:
        """Returns what is cost to throw food away depending of the temperature inside the fridge.

        Returns
        -------
        float
            The cost to throw food away.
        
        Note
        ----
        You should not call this method. 
        
        References
        ----------
        [1] (T. Kallehauge, M. V. Vejling, J. J. Nielsen, 2022, pp 2)
        
        Examples
        --------
        >>> Fridge().__food_expense()
        0
        """
        if self.__t[self.__n-1] < 3.5:
            return 4.39*exp(-0.49*self.__t[self.__n-1])
        elif self.__t[self.__n-1] >= 6.5:
            return 0.11*exp(0.31*self.__t[self.__n-1])
        else:
            return 0

    def simulate(self) -> float:
        """Returns a float of the operating cost. 

        Returns
        -------
        float
            The cost in DKK.
        
        References
        ----------
        [1] (T. Kallehauge, M. V. Vejling, J. J. Nielsen, 2022, pp 4)

        Examples
        --------
        >>> Fridge().simulate()
        13813.11500000001
        """
        self.__t = append(self.__t, self.__T_START)
        self.__expense = append(self.__expense, 0)

        for self.__n in arange(1, self.__N):
            self.__thermostat_smart_result = self.__thermostat_smart()

            self.__t = append(self.__t, self.__t[self.__n-1] + (self.__c_1()*(self.__T_ROOM - self.__t[self.__n-1]) + self.__c_2()*(self.__T_COMPRESSOR - self.__t[self.__n-1]))*self.__DELTA_T)
            self.__expense = append(self.__expense, self.__expense[self.__n-1] + self.__power_expense() + self.__food_expense())

        try:
            return self.__expense[-1]
        finally:
            self.__expense = delete(self.__expense, slice(0 ,len(self.__expense)))
            self.__t = delete(self.__t, slice(0, len(self.__expense)))
        

if __name__ == "__main__":
    print(Fridge(SMART=True).simulate())
    # import doctest
    # doctest.testmod()
