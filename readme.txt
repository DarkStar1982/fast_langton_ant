README
=========TASK DESCRIPTIONS==========
Consider an infinite grid of white and black squares. The grid is initially all white and there is a machine
in one cell facing right. It will move based on the following rules:
* If the machine is in a white square, turn 90° clockwise and move forward 1 unit;
* If the machine is in a black square, turn 90° counter-clockwise and move forward 1 unit;
* At every move flip the color of the base square.

=========ASSUMPTIONS================
* Can be run on *nix box without extra libraries using Python 2 definitions
* Performance of the simulation is important, in both cpu and & i/o
* No validation on inputs
* Saves output in plaintext file - '.' as white cell, and '*' as black cell
* Minimilistic extra functionality - only does what is requested and no more

========HOW TO USE==================
* Implemented as command line utility, with a standard format of commands
* On Mac specify port number above 1024 (due OS restrictions)
* Example call
