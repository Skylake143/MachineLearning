from pathlib import Path
import runpy
from multiprocessing import Process
import argparse
import sys

"""
YOU CAN CHANGE THE FLAGS BELOW TO FIT YOUR NEEDS.
"""

# if filename start with "student" set this variable to true, if it starts with a number set it to false.
FILENAME_FORMAT_STUDENT = True
# This determines if the unittest for all student should be run automatically.
EXECUTE = True
# This flag determines if the files are run in parallel or sequential.
RUN_PARALLEL = True
# Maximum run time per student (This can be more if students before this student are also slow).
# This kicks in when a students code is not done when checking their process status.
# Therefore, this is a maximum runtime after checking if the test are done.
# Note, that this is a really bad way to limit runtime for students and should only be used to avoid endless loops or deadlocks.
MAX_RUNTIME = 1

# Create Argument Parser
parser = argparse.ArgumentParser(description='Argument Parser for Script.py')

# Add arguments with default values
parser.add_argument('--FILENAME_FORMAT_STUDENT', type=bool, default=FILENAME_FORMAT_STUDENT,
                    help='Set to True if the filename starts with "student"; False if it starts with a number')
parser.add_argument('--EXECUTE', type=bool, default=EXECUTE,
                    help='Determines if the unit tests for all students should run automatically')
parser.add_argument('--RUN_PARALLEL', type=bool, default=RUN_PARALLEL,
                    help='Flag to run the files in parallel or sequentially')
parser.add_argument('--MAX_RUNTIME', type=int, default=MAX_RUNTIME,
                    help='Maximum runtime for the unittest after checking if they are done.'
                         'This is purely to avoid endless loops or deadlocks')

# Parse arguments
args = parser.parse_args()

# Update the variables with the parsed arguments
FILENAME_FORMAT_STUDENT = args.FILENAME_FORMAT_STUDENT
EXECUTE = args.EXECUTE
RUN_PARALLEL = args.RUN_PARALLEL
MAX_RUNTIME = args.MAX_RUNTIME

# The script that needs to be appended to each student file.
SCRIPT = \
"""
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
"""

def run_student_code(file):
    # This makes python think that the student code is run from the terminal.
    module_path = file.relative_to(Path(sys.argv[0]).resolve().parent)
    module_path = module_path.with_suffix('').as_posix().replace("/",".")
    runpy.run_module(mod_name=module_path, run_name='__main__', alter_sys=True)

def extend_file(file):
    with open(file, "r+") as f:
        # check if the SCRIPT is already added.
        if SCRIPT not in f.read():
            f.write(SCRIPT)

    if EXECUTE:
        # Start a new process for each students such that the unittest file can import a different student "module/script".
        p = Process(name=str(file), target=run_student_code, args=(file,))
        p.start()
        if not RUN_PARALLEL:
            p.join()
        return p

if __name__ == "__main__":
    # The current directory
    dir = Path(__file__).parents[0]

    # Go through all the student files.
    processes = []
    if FILENAME_FORMAT_STUDENT:
        for file in dir.glob("**/student*.py"):
            p = extend_file(file)
            processes.append(p)
    else:
        for file in dir.glob(f"**/{'[0-9]'*6}*.py"):
            p = extend_file(file)
            processes.append(p)

    # close all processes, thus unittests
    for p in processes:
        # check if tests for a student is done
        if p.is_alive():
            # Give the test 10 seconds to finish running
            p.join(MAX_RUNTIME)

            # force the tests to stop running
            if p.is_alive():
                p.terminate()
                p.join()

                # Create the file path to store the results
                dir = Path(p.name).parents[0] / "test_results"
                path = dir / Path(p.name).stem
                path = path.with_suffix('.txt')

                with open((path), "a") as log_file:
                    log_file.write(f"\n...\n\nThe rest of the unittest are terminate due to exceeding the maximum runtime of {MAX_RUNTIME} seconds.")