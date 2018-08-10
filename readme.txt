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

========LIMITATIONS==================
* No validation on HTTP inputs
* Saves output in plaintext file - '.' as white cell, and '*' as black cell, can be easily replaced with other symbols
* Minimalistic functionality with no extras - only does what is requested and no more
* filename is included in the request body - stored in the same directory
* No out of memory or out of disk precautions - can definitely run out of both on large number of steps requested

========HOW TO USE==================
* Implemented as command line utility, with a standard command format convention
* On Mac specify port number above 1024 (due OS restrictions)
* Example call to run as a server:
  "server.py -p 8081"
* Example client call
  curl -X PUT -H "Content-Type: application/json" -d '{"run_steps":5, "filename":"test.txt"}' "localhost:8081"
