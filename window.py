import numpy as np

class Window:
    def __init__(self, arr):
        self.arr = arr
        self.size = arr.size
        self.pos = 0

    def update(self, new_val):
        self.arr[self.pos] = new_val
        self.pos += 1
        if self.pos >= self.size:
            self.pos = 0
