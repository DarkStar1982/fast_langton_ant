#!/usr/bin/python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from json import loads
from time import time
import sys
import getopt

# program wide options
OPTIONS = {
    "nofile":False,
    "port": 8080
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
            0:  [0,1],  # up
            90: [1,0],  # right
            180:[0,-1], # down
            270:[-1,0], # left
        }

    def run_steps(self, steps):
        for i in range(0,steps):
            # check local position and rotate counterclockwise (can go negative)
            # or clockwise (always positive) in 90 deg increments, and flip color
            if (self.machine["pos_x"],self.machine["pos_y"]) in self.black_cell_dict:
                self.machine["angle"] = (self.machine["angle"] - 90) % 360
                del self.black_cell_dict[(self.machine["pos_x"],self.machine["pos_y"])]
            else:
                self.machine["angle"] = (self.machine["angle"] + 90) % 360
                self.black_cell_dict[(self.machine["pos_x"],self.machine["pos_y"])] = 1
            # advance one unit in the current direction
            self.machine["pos_x"] = self.machine["pos_x"] + self.moves[self.machine["angle"]][0]
            self.machine["pos_y"] = self.machine["pos_y"] + self.moves[self.machine["angle"]][1]
            # update bounding box
            self.bounding_box["max_x"] = max(self.machine["pos_x"], self.bounding_box["max_x"])
            self.bounding_box["max_y"] = max(self.machine["pos_y"], self.bounding_box["max_y"])
            self.bounding_box["min_x"] = min(self.machine["pos_x"], self.bounding_box["min_x"])
            self.bounding_box["min_y"] = min(self.machine["pos_y"], self.bounding_box["min_y"])

    def dump_to_file(self, filename):
        # recalculate coordinate range from -x..x, -y..y to 0..X, 0..Y
        offset_max_x = self.bounding_box["max_x"] - self.bounding_box["min_x"]
        offset_max_y = self.bounding_box["max_y"] - self.bounding_box["min_y"]
        # pass one - write down the empty field
        file = open(filename, "w")
        p_line = bytearray('.' * (offset_max_x+1))
        for y in range(offset_max_y, -1, -1):
            file.write(p_line)
            file.write("\n")
        file.close()
        # pass two - write down the black cells
        file = open(filename, "r+")
        line_length = offset_max_x+2
        file_length = line_length*offset_max_y
        for item in self.black_cell_dict.keys():
            x = item[0] - self.bounding_box["min_x"]
            y = item[1] - self.bounding_box["min_y"]
            file.seek(file_length-y*line_length+x)
            file.write('*')
        file.close()
        return file_length

class PUTHandler(BaseHTTPRequestHandler):
    def do_put(self):
        length = self.headers['Content-Length']
        content = self.rfile.read(int(length))
        request_data = loads(content)
        if "run_steps" in request_data and "filename" in request_data:
            simulator = Simulator()
            start_time = time()
            simulator.run_steps(request_data["run_steps"])
            print "%4.1f steps per second" % (request_data["run_steps"]/(time() - start_time))
            if not OPTIONS["nofile"]:
                start_time = time()
                bytes_written = simulator.dump_to_file(request_data["filename"])
                io_speed = bytes_written/(time() - start_time)
                print "%4.1f MB per second average written" % (io_speed/1.0E6)
            self.send_response(200)
        else:
            self.send_response(400)

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hnp:",["help","nofile","port=",])
    except getopt.GetoptError:
        print ('server.py --help')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print "Specify server port with -p <port number> or --port <port number>"
            print "Default port number is 8080"
            sys.exit(0)
        if opt in ('-n','--nofile'):
            OPTIONS["nofile"] = True
        elif opt in ('-p','--port'):
            OPTIONS["port"] = int(arg)
    # run HTTP request server
    instance = ('localhost', OPTIONS["port"])
    http_server = HTTPServer(instance, PUTHandler)
    http_server.serve_forever()

main(sys.argv[1:])
