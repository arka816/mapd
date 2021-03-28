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

 - The first line inputs the dimensions of the grid, where 6 is the number of rows and 17 is the number of columns.
- The next 6 lines contain 17 space separated integers each, providing the details of the grid where 1 signifies **normal cells**, 2 signifies **temporary storages** and 0 signifies **blocked cells** or obstacles.
- The next line contains one integer denoting the number of robots.
- The next 3 lines contain 4 space-separated integers each, where first two are the coordinates of the starting point and next two (0,8) are the coordinates of the ending point of each of the 3 robots.
- The next line contains one integer, denoting number of tasks to be completed (3 in this case).
- The next 3 lines contain 4 space-separated integers each, where first two are the coordinates of the pickup point and next two (0,8) are the coordinates of the drop-off point of each of the 3 tasks respectively.
### Format of output

    approximate makespan:  26
    optimal allocation: 
    Agent 0 : [0]
    Agent 1 : [2]
    Agent 2 : [1]
    
  Here the output reports the approximate make-span and the optimal allocation for each of the agents as a list of tasks.
