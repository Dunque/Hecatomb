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
menu:
	$(PYTHON) $(FILE) $@

# Level1
l1:
	$(PYTHON) $(FILE) $@

# Level2
l2:
	$(PYTHON) $(FILE) $@

# Level3
l3:
	$(PYTHON) $(FILE) $@

# Pause (sobre Cutscene1)
pause:
	$(PYTHON) $(FILE) $@

#------------------------------------------------
