FILE = main.py

all: run

run:
	python3 $(FILE)

run2:
	python3 $(FILE) &

1:
	python3 $(FILE) $@

2:
	python3 $(FILE) $@

3:
	python3 $(FILE) $@
