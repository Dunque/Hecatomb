PYTHON = python3
FILE = main.py

all: run

run:
	$(PYTHON) $(FILE)

run2:
	$(PYTHON) $(FILE) &

clean:
	find . -name '__pycache__' -type d | xargs rm -fr
