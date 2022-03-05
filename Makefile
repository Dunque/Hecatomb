PYTHON = python3
FILE = main.py

all: run

run:
	$(PYTHON) $(FILE)

run2:
	$(PYTHON) $(FILE) &

clean:
	find . -name '__pycache__' -type d | xargs rm -fr

#------------------------------------------------
# Menu
0:
	$(PYTHON) $(FILE) $@

# Level1
1:
	$(PYTHON) $(FILE) $@

# Level2
2:
	$(PYTHON) $(FILE) $@

# Level3
3:
	$(PYTHON) $(FILE) $@
#------------------------------------------------
