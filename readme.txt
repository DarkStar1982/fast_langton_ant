=========INTRODUCTON==========

An implementation of Langton's ant algorithm.
Useful as a simple benchmark tool to test CPU and I/O performance.

=========ALGORITHM DESCRIPTION==========
Consider an infinite grid of white and black squares. The grid is initially all white and there is a machine
in one cell facing right. It will move based on the following rules:
* If the machine is in a white square, turn 90° clockwise and move forward 1 unit;
* If the machine is in a black square, turn 90° counter-clockwise and move forward 1 unit;
* At every move flip the color of the base square.

========HOW TO USE==================
* A command line utility, with a standard options format
* Use example:
  "server.py -s <generations> -f <filename>" will run the simulation for a number of generations specified
  and save the result in the file provided.
* Watch out for disk space - for 10M generations save file will be around 36 GB.
