# Find a global minimum

Demonstrate attempts to find a global minimum with concurrent techniques in Python.

* [process-main.py](find-min/process-main.py) - uses multiprocessing.Process to spawn out processes with each process working on
  a subset of larger dataset.

* [pool-main.py](find-min/pool-main.py) - uses multiprocessing.Pool to farm out works to a pool of workers. Number of worker processes are
  constrainted by number of available workers created for the pool.

