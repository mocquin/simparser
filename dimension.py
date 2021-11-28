from collections import Counter
import numpy as np

class BasicDimension():
    
    def __init__(self, string_or_counter):

        if type(string_or_counter) == Counter:
            self.counter = string_or_counter
        elif type(string_or_counter) == str:
            self.counter = Counter({string_or_counter:1})
        elif type(string_or_counter) == dict:
            self.counter = Counter(string_or_counter)

        else:
            raise ValueError(f"for {string_or_counter}")
            
    def __str__(self):
        return f"BasicDimension({self.counter})"
    
    def __repr__(self):
        return f"BasicDimension({self.counter})"
        
    def __mul__(self, y):
        """Allow the multiplication of Dimension objects."""
        self.counter.update(y.counter)
        return BasicDimension(self.counter)

    __rmul__ = __mul__
    
    def __truediv__(self, y):
        """Allow the division of Dimension objects."""
        self.counter.subtract(y.counter)
        return BasicDimension(self.counter)

    def __rtruediv__(self, x):
        """Only used to raise a TypeError."""
        return self**-1

    def __pow__(self, y):
        """Allow the elevation of Dimension objects to a real power."""
        return BasicDimension(Counter({k:v*y for k,v in self.counter.items()}))
    
if __name__ == "__main__":
    a = Counter({'L': 1, 'T': -1})
    b = Counter({'T': 1})
    c = a.subtract(b)
    #print(c)
    
    L = BasicDimension("L")
    T = BasicDimension("T")
    speed = BasicDimension({"L":1, "T":-1})
    acc = speed/T
    print(acc)
    print(acc**2)
    print(1/acc)
    print(acc*acc)

    