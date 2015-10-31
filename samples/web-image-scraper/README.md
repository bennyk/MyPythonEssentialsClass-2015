

This folder contains a list of sample code that demonstrate the use of variety of Python modules to dispatch
a list of downloading jobs concurrently. Image URLs are scraped from a given website to generate a download task.

1. fork-main.py - Demonstrate the use of fork to dispatch a list of download task.

2. subprocess-main.py - Demonstrate how to spawn a list of subprocesses using subprocess module and curl utility to
   download a remote URL resource.
   
3. multi-main.py - Demonstrate how to dispatch multiple URL downloading task using multiprocessing.Process.

4. multi-queue-main.py - Demonstrate the use of multiprocessing.Queue to manage a list of URL downloading task. A list
   of workers are pre-spawned to handle the downloading workload independently.
   
5. multi-pool-main.py - Demonstrate how to dispatch a list of URL downloading tasks to a pool of workers managed by
   multiprocessing.Pool. Workloads can be further fine-tuned by the use of chunksize.
