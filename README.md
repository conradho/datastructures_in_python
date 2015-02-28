Testing
=======
- run `python3.4 -m unittest` from the project root dir to check that all tests pass


Profiling
=========
- Note Bene: need to monitor system cpu, memory, network load etc while profiling to make sure nothing else is interfering
- have your own hypothesis before profiling
- just `print(time.time())`
	- can wrap functions in decorators with print statements before and after
- on command line:
	- `python -m timeit -s "import your_module" "your_module.call_function()"`
	- `/usr/bin/time --verbose python your_code.py`   <-- don't confuse this with bash/shell time
		- page faults == having to load data from disk because it got pushed out of RAM
	- `python -m cProfile -s cumulative your_code.py`
		- note how much overhead cProfile creates
		- see if the # of times each function was called is what you estimated
