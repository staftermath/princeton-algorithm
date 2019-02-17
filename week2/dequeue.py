"""
 A double-ended queue or deque (pronounced “deck”) is a generalization of 
 a stack and a queue that supports adding and removing items from either the 
 front or the back of the data structure. 

 The implementation uses amortized array size adjustment

 This file create a generic data type Deque that implements the following API:

class Deque {
   boolean is_empty()                 // is the deque empty?
   int size                          // return the number of items on the deque
   void add_first(Item item)          // add the item to the front
   void add_last(Item item)           // add the item to the end
   Item remove_first()                // remove and return the item from the front
   Item remove_last()                 // remove and return the item from the end
   __iter__()                         // return an iterator
}
"""
import random

class Deque(object):
    def __init__(self, x=None):
        self._size = 0
        self._array = [None]*4
        self._begin = 1
        self._end = self._begin+self._size
        if x is not None and isinstance(x, list) and len(x) > 0:
            for item in x:
                self.add_last(item)        

    def is_empty(self):
        return self._size == 0

    @property
    def size(self):
        return self._size

    def add_first(self, value):
        if self.is_empty():
            self._size += 1
            self._array[self._begin] = value
            self._end = self._begin + self._size
        else:
            self._size += 1
            self._array[self._begin-1] = value
            self._begin -= 1
        buffer_size = len(self._array)
        if self._begin == 0:
            self._array = [None]*buffer_size+self._array
            self._begin += buffer_size
            self._end += buffer_size

    def add_last(self, value):
        self._array[self._end] = value
        self._end += 1
        self._size += 1
        buffer_size = len(self._array)
        if self._end == buffer_size:
            self._array = self._array+[None]*buffer_size

    def remove_first(self):
        if self._array[self._begin] is None:
            raise ValueError("Deque is empty")
        result = self._array[self._begin]
        self._array[self._begin] = None
        self._begin += 1
        self._size -= 1
        half_buffer_size = len(self._array)//2
        if self._begin >= half_buffer_size:
            self._array = self._array[half_buffer_size//2:]
            self._begin -= half_buffer_size//2
            self._end -= half_buffer_size//2
        return result

    def remove_last(self):
        if self._array[self._end-1] is None:
            raise ValueError("Deque is empty")
        result = self._array[self._end-1]
        self._array[self._end-1] = None
        self._end -= 1
        self._size -= 1
        half_buffer_size = len(self._array)//2
        if len(self._array)-self._end >= half_buffer_size:
            self._array = self._array[:(len(self._array)-half_buffer_size//2)]
        return result

    def __iter__(self):
        return self._array[self._begin:self._end].__iter__()

class RandomDeque(Deque):
    def __init__(self, x=None):
        super(RandomDeque, self).__init__(x=x)
    
    def sample(self):
        return random.choice(self._array[self._begin:self._end])