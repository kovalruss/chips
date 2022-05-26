BASH=bash -l -c

chips_add:
	python -m chips.add

chips_remove:
	python -m chips.remove

results:
	python -m chips.results

run_case1:
	python -m test_.testcase1

run_case2:
	python -m test_.insio.testcase2