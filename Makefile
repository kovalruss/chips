BASH=bash -l -c

chips_add:
	python -m chips -a

chips_remove:
	python -m chips -r

results:
	python -m chips -g

run_case1:
	python -m test_.testcase1

run_case2:
	python -m test_.insio.testcase2

run_case3:
	python -m test_2_.testcase3