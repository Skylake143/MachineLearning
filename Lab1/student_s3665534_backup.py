############ CODE BLOCK 0 ################
# ^ DO NOT CHANGE THIS LINE


# Import everything in one cell
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Note: if this gives you errors, then scroll down to the section on environments

############ CODE BLOCK 1 ################
# ^ DO NOT CHANGE THIS LINE

#Implement your method here
def hello(word):
    # raise NotImplementedError('Your code here')
    return f'Hello {word.capitalize()}!'

############ CODE BLOCK 2 ################
# ^ DO NOT CHANGE THIS LINE 

def roll_array(array, steps, direction='left'):
    '''Roll the contents of a 1D array, "steps" steps in the given direction, wrapping around. '''
    # raise NotImplementedError('Your code here')
    if direction=='right': steps = -steps
    left = array[steps:]
    right = array[:steps]
    rolled_array = np.concatenate((left,right))
    return rolled_array


# THE CODE BELOW IS AUTO GRADES THE FILE, THIS CODE IS ALSO AUTOMATICALLY ADDED.
# DO NOT CHANGE THE CODE BELOW, OTHERWISE THE SCRIPT KEEPS ADDING THE SAME CODE.
if __name__ == "__main__":
    from unit_test import *
    from pathlib import Path
    
    # Create the file path to store the results
    dir = Path(__file__).parents[0] / "test_results"
    Path(dir).mkdir(parents=True, exist_ok=True) 
    path = dir / Path(__file__).stem
    path = path.with_suffix('.txt')
    
    # Run the tests
    with open((path), "w") as log_file:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestClass)
        unittest.TextTestRunner(stream=log_file, verbosity=2).run(suite)
