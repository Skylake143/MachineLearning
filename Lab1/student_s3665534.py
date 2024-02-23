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

############ CODE BLOCK 3 ################
# ^DO NOT CHANGE THIS LINE

#Implement your method here
def surface_class(frame, min_surface):
    ''' Return the class labels of all rows with a surface >= least min_surface '''
    #raise NotImplementedError('Your code here')
    labels = frame.loc[frame['height'] * frame['width'] >= min_surface]['class_labels']
    return labels

############ CODE BLOCK 4 ################
# ^ DO NOT CHANGE THIS LINE
 
def generate_data(
    amount=100, proportion=0.7, # By default we want 70% class a, 30% class b
    signal_a_height=5, signal_a_width=10, a_noise=2,
    signal_b_height=4, signal_b_width=6, b_noise=3,
    random_state=42  # by default, always generate the same data
):
    if random_state is not None:
        np.random.seed(random_state)
    
    # Calculate how many instances of each class to generate
    a_amount = int(amount * proportion)
    b_amount = amount - a_amount
    
    # Generate instances of class a
    # The height and width are the sum of signal + noise
    a_height = signal_a_height + (np.random.randn(a_amount) * a_noise)
    a_width = signal_a_width + (np.random.randn(a_amount) * a_noise)
    a_labels = np.full(a_amount, 'a')
    
    # Do the same for b
    b_height = signal_b_height + (np.random.randn(b_amount) * b_noise)
    b_width = signal_b_width + (np.random.randn(b_amount) * b_noise)
    b_labels = np.full(b_amount, 'b')

    # Wrap it up in a nice dataframe
    df = pd.DataFrame({
        'height': np.concatenate([a_height, b_height]),
        'width': np.concatenate([a_width, b_width]),
        'label': np.concatenate([a_labels, b_labels])
    })
    return df

############ CODE BLOCK 5 ################
#^ DO NOT CHANGE THIS LINE

class OneNearestNeighborClassifier:
    def __init__(self):
        self.y_train = None
        self.x_train = None

    def fit(self, x_train, y_train):
        """ To fit, we just store the entire training data. """
        self.x_train = x_train
        self.y_train = y_train

    def distance(self, a, b):
        """ Return the Euclidean distance between point a and b """
        return np.sqrt(np.sum((a - b)**2))

    def predict(self, x_test):
        """ Predict the label of test instances 
        
        For each test instance, find the nearest point in the training set.
        Then return a list of the labels of the nearest points that you found.
        """
        prediction = []
        #prediction = np.full(x_test.shape[0], self.majority_label)
        
        for index_prediction, x in enumerate(x_test.values): 
            min_distance = np.inf
            label = None
            for index, x_compare in enumerate(self.x_train.values): 
                dist = self.distance(x, x_compare)
                if dist <  min_distance: 
                    min_distance = dist
                    label = y_train[index]
            prediction.append(label)


        if isinstance(x_test, pd.DataFrame):
            return pd.Series(prediction)
        return np.asarray(prediction)  # as a numpy array


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
