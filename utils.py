
import numpy as np

class FrozenClass(object):
    __isfrozen = False
    __islocked = False
    def __setattr__(self, key, value=None):
        if self.__isfrozen:
            if  not hasattr(self, key):
                raise TypeError( "%r is a frozen class" % self )
            
            if self.__islocked and value is not None:
                raise TypeError( "%r has been locked. Modifying its attributes is no longer possible" % self)
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__isfrozen = True
    def lock(self):
        self.__islocked = True

class circle(FrozenClass):
    def __init__(self, *args, **kwargs):
        self.update_values(*args, **kwargs)
        self._freeze()

    def update_values(self, radius = None, diameter=None, area=None):
        isgiven = np.array([x is not None for x in [radius, diameter, area]])
        assert np.sum(isgiven) <= 1, "overdetermined circle"
        assert np.sum(isgiven) >0, "please give at least one parameter"
        self._r = radius
        self._d = diameter
        self._A = area
        self._is_update = isgiven

        self.calc_r()
        self.calc_A()
        self.calc_d()

        
    
    def calc_r(self):
        if self._is_update[0]:
            return
        
        if self._d is not None:
            self._r = self._d/2
        elif self._A is not None:
            self._r = np.sqrt(self._A/np.pi)
        
        self._is_update[0] = True
    
    def calc_d(self):
        if self._is_update[1]:
            return 
        
        self.calc_r()
        if self._r is not None:
            self._d = self._r*2

        self._is_update[1] = True

    def calc_A(self):
        if self._is_update[2]:
            return
        
        self.calc_r()
        if self._r is not None:
            self._A = np.pi * self._r**2

        self._is_update[2] = True

    def r(self):
        return self._r

    def d(self):
        return self._d
    
    def A(self):
        return self._A
    
    



class func_saver:
    def __init__(self, func):
        self.set_func(func)
        self.storef = []
        self.storex = []

    def flush(self):
        self.storef = []
        self.storex = []


    def set_func(self, func):
        self.function = func

    def __call__(self, *args, **kwargs):
        f = self.function(*args, **kwargs)
        self.storef.append(f)
        x = args
        if kwargs:
            x = [x, kwargs]
        self.storex.append(x)

        return f

def shrink_interval(interval, ratio):
    interval = np.array(interval, dtype = np.float64)
    assert interval.shape == (2,)
    m = interval.mean()
    r = (interval[1]-interval[0])/2
    return np.array([m-r*ratio ,m+r*ratio])

