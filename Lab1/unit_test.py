import unittest
import sys
from pathlib import Path
import numpy as np
import pandas as pd


"""
Some magic to import your code (assignment) into this file for testing.
Please do not change the code below.
"""
# import the specific student code
student_file = Path(sys.argv[0])
sys.path.append(str(student_file.parent))

# import student code
m = __import__(student_file.stem)

# find all imports, either with __all__ or dir
try:
    attrlist = m.__all__
except AttributeError:
    attrlist = dir(m)

# add all student code to this namespace.
for attr in attrlist:
    if attr[:2] != "__":
        globals()[attr] = getattr(m, attr)

"""
PLEASE do not change the code above, you can add code if you want.
"""

class TestClass(unittest.TestCase):

    def test_hello(self):
        self.assertEqual(hello("World"), 'Hello World!')
        self.assertEqual(hello("you"), "Hello You!")

    def test_roll_array(self):
        a = np.arange(10)
        self.assertTrue(np.array_equal(roll_array(a,2,"right"), np.asarray([8, 9, 0, 1, 2, 3, 4, 5, 6, 7])))
        self.assertTrue(np.array_equal(roll_array(a,4,"left"), np.asarray([4, 5, 6, 7, 8, 9, 0, 1, 2, 3])))

    def test_surface_class(self):
        df = pd.DataFrame({
            'height':[1, 2, 3, 4, 5], 
            'width':[5, 4, 8, 10, 1], 
            'class_labels': ['a', 'b', 'c', 'a', 'a']
        })
        
        labels = np.asarray(surface_class(df, 24))
        target = np.asarray(['c', 'a'])
        self.assertTrue(np.array_equal(labels, target), f"{labels} != {target}")

        labels = np.asarray(surface_class(df, 25))
        target = np.asarray(['a'])
        self.assertTrue(np.array_equal(labels, target), f"{labels} != {target}")
    
    def test_OneNearestNeighborClassifier(self):
        train = generate_data()
        x_train = train[['height', 'width']]
        y_train = train['label']
        
         # Make some new data to test with
        test = generate_data(random_state=43)  # we want different test data
        x_test = test[['height', 'width']]
        y_test = test['label']

        classifier = OneNearestNeighborClassifier()
        classifier.fit(x_train, y_train)  # Learn from the training data

        prediction = classifier.predict(x_test)  # Make a prediction about the test data

        accuracy = np.sum(y_test == prediction) / len(y_test)
        target_accuracy = 0.75

        self.assertTrue( accuracy >= target_accuracy, f'Accuracy {accuracy} != {target_accuracy}')
