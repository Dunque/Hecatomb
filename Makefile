FILE = main.py

all: run

run:
	python3 $(FILE)

run2:
	python3 $(FILE) &
