Description of algorithm and modifications done to alpha beta- 
The approach is essentially the same as classic alpha beta pruning algorithm with one little difference, The Max search and the min search return a tuple containing (v,action) rather than only v. The recursive calls by min and max to each other discard the action from the value returned as they don't need it. The top level apha beta search keeps the action returned by Max and returns it.

Description of Evaluation function- 

The Heuristic evaluates a board position according to following criteria - 
possible wins = total no of open rows , cols or diagonals where a symbol can win. (only those rows,cols or diagonals are evaluated which have the symbol present in them, empty row or diagonal is not counted)

AI plays MAX, therefore the value returned for a particular board position is 
		possiblewinsAI – possiblewinsHuman

Description of implementation- The project is implemented in python and tested with both linux and windows. The GUI library used is 'wx python'.

Instructions to run:
	Prerequesites- 
		1. Python 2.7
		2. wx python library
Instructions to install wx-python
1. Determine the installation type of the python runtime, 32 bit or 64 bit and install the wx python library
2. According to environment install one of the following setups
For windows - http://www.wxpython.org/download.php


For Ubuntu and similar versions of linux -  sudo apt-get install python-wxgtk2.8
3. Put the following files in one folder
	ai.py
	gui.py

run the command from the terminal to start the game: python ai.py