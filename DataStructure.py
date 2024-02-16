"""! @brief The DataStructure package.
"""

##
# @file DataStructure.py
#
# @brief This package defines the required data structure classes.
#
# @section description_datastructure Description
# This package provides the data structure required for the audio processing project. i.e., the Array class. Note that you will use Array throughout the entire semester, so you need to practice using the Array data structure. The Array class has two attributes. _cap stores the array's capacity, i.e., the maximum number of items that can be stored in the array. _data is a Python list used as the container to store items in an array. Remark: noticing the difference between an array and a Python list is important. e.g., you cannot use [-1] to access the last item in an array. Instead, you need to use [len(array) - 1]. Furthermore, Array has no append, insert methods.
#
# @section libraries_datastructure Libraries/Modules
# - typing (from the standard library)
#   - Access to Any.
#
# @section notes_datastructure Notes
# - Comments should be Doxygen compatible.
#
# @section todo_datastructure TODO
# - None. You should not need to modify this file. If you do, write it down in the README and let us know why you need to make the changes.
#
# @section author_array Author(s)
# - Created by SingChun Lee on 12/24/2023
# - Modified by SingChun Lee on 12/30/2023
#
# Copyright (c) 2023 Bucknell University. All rights reserved.

from typing import Any

class Array:
    """! The DataStructure.Array class.
    
    Defines the basic array class.
    """
    
    def __init__(self, cap: int = 10, init_val = None) -> None:
        """! The array class initializer.
        
        @param cap The capacity of the array.
        
        @param init_val The value used to initialize the array. Default is None.
        """
        
        ## The capacity of the array
        self._cap = cap
        ## The array data, stored using a Pythong list
        self._data = [init_val for _ in range(self._cap)] 
        
    def __str__(self) -> str:
        """! A string representation of the array.
        
        @return A string that represents the array.
        """
        
        s = ''
        for elm in self._data:
            s += str(elm) + ", "
        return '[' + s.rstrip().rstrip(',') + ']'
        
    def __len__(self) -> int:
        """! The array length function.
        
        @return The length/capacity of the array.
        """
        
        return self._cap
        
    def _boundary_check(self, index: int) -> None:
        """! Check if an index is in bound, raise an error if not.
        
        @param index The input index.
        """
        
        if index < 0 or index >= self._cap:
            raise IndexError
        
    def __getitem__(self, index: int) -> Any:
        """! Get the item stored at index in the array.
        
        @param index The input index.
        
        @return The item stored at index.
        """
        
        self._boundary_check(index)
        return self._data[index]
        
    def __setitem__(self, index: int, value: Any):
        """! Store the input value at index in the array.
        
        @param index The input index.
        
        @param value The input value.
        """
        
        self._boundary_check(index)
        self._data[index] = value
