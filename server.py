#!/usr/bin/python
from time import time
import sys, getopt

OPTIONS = {
    "nofile":False,
    "filename":"test.txt",
    "steps":0
}

class Simulator(object):
    def __init__(self):
        self.black_cell_dict = {}
        self.machine = { "angle":90, "pos_x":0, "pos_y":0 }
        self.bounding_box = {
            "min_x":0, "min_y":0,
            "max_y":0, "max_x":0,
        }
        self.moves = {
            0:  [0,  1], 90: [ 1, 0],  # up right
            180:[0, -1], 270:[-1, 0],  # down left
        }

    def run_steps(self, steps):
        i = 0
        while (i < steps):
            if (self.machine["pos_x"],self.machine["pos_y"]) in self.black_cell_dict:
                self.machine["angle"] = (self.machine["angle"] - 90) % 360
                del self.black_cell_dict[(self.machine["pos_x"],self.machine["pos_y"])]
            else:
                self.machine["angle"] = (self.machine["angle"] + 90) % 360
                self.black_cell_dict[(self.machine["pos_x"],self.machine["pos_y"])] = 1
            self.machine["pos_x"] = self.machine["pos_x"] + self.moves[self.machine["angle"]][0]
            self.machine["pos_y"] = self.machine["pos_y"] + self.moves[self.machine["angle"]][1]
            self.bounding_box["max_x"] = max(self.machine["pos_x"], self.bounding_box["max_x"])
            self.bounding_box["max_y"] = max(self.machine["pos_y"], self.bounding_box["max_y"])
            self.bounding_box["min_x"] = min(self.machine["pos_x"], self.bounding_box["min_x"])
            self.bounding_box["min_y"] = min(self.machine["pos_y"], self.bounding_box["min_y"])
            i = i + 1
        self.offset_max_x = self.bounding_box["max_x"] - self.bounding_box["min_x"]
        self.offset_max_y = self.bounding_box["max_y"] - self.bounding_box["min_y"]

    def dump_to_file(self, filename):
        file = open(filename, "w")
        p_line = '.' * (self.offset_max_x+1)
        for y in range(self.offset_max_y, -1, -1):
            file.write(p_line)
            file.write("\n")
        file.close()
        file = open(filename, "r+")
        line_length = self.offset_max_x+2
        file_length = line_length*self.offset_max_y
        for item in self.black_cell_dict.keys():
            x = item[0] - self.bounding_box["min_x"]
            y = item[1] - self.bounding_box["min_y"]
            file.seek(file_length-y*line_length+x)
            file.write('*')
        file.close()
        return file_length

def run_benchmark():
    simulator = Simulator()
    start_time = time()
    simulator.run_steps(OPTIONS["steps"])
    print ("CPU performance: %4.2fK gen/s" % ((OPTIONS["steps"]/1000)/(time() - start_time)))
    if not OPTIONS["nofile"]:
        start_time = time()
        bytes_written = simulator.dump_to_file(OPTIONS["filename"])
        end_time = time()
        io_speed = ((bytes_written)/(end_time - start_time))/1.048576E6
        print ("I/O performance: %4.2f MB/s " % io_speed)

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hns:f:",["help","nofile","steps=","file="])
    except getopt.GetoptError:
        print ('server.py --help')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print ("Langton's ant algorithm implementation.")
            print ("\tUse as: 'server.py -s <generations> -f <filename>'. This will run the simulation")
            print ("\tfor a number of generations specified and save the result in the file provided.")
            print ("\tSpecifying -n or --nofile option doesn't save simulation result to disk.")
            sys.exit(0)
        elif opt in ('-n','--nofile'):
            OPTIONS["nofile"] = True
        elif opt in ('-s','--steps'):
            OPTIONS["steps"] = int(arg)
        elif opt in ('-f','--file'):
            OPTIONS["filename"] = arg
    run_benchmark()

main(sys.argv[1:])
