# AIFA: Multi Agent Path Finding

The question in the assignment revolves around Multi Agent path Finding with pickup and delivery.
The .py files **mapd_heuristic.py** and **mapd_optimal.py** provide the heuristic and optimal solutions respectively. 
## Execution and test files
The file can be executed in the terminal as:
**python file_name.py test_filename.task**
A sample test file namely **demo.task** has been provided and would be parsed as default if **test_filename.task** is not provided in the CLI.
It is advised to provide the complete address of the task file in the terminal during execution.
### Format of input in demo.task

    6 17
    1 1 1 1 1 2 1 1 1 1 2 1 1 0 1 1 1
    1 1 1 1 1 1 1 1 1 1 1 1 2 1 1 1 1
    1 0 1 1 1 1 2 1 1 2 1 1 1 1 1 0 1
    1 1 1 2 1 1 1 1 1 1 1 1 2 1 1 1 1
    1 1 1 1 1 1 2 1 1 1 0 1 1 1 1 1 2
    2 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1
    3
    0 0 0 8
    5 9 5 5
    0 0 5 5
    3
    5 0 3 12
    4 6 0 5
    5 0 0 5