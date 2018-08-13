#!/usr/bin/python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from json import loads
from time import time
import sys, getopt

OPTIONS = {
    "nofile":False,
    "port": 8080,
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

class PUTHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        length = self.headers['Content-Length']
        content = self.rfile.read(int(length))
        request_data = loads(content)
        if "run_steps" in request_data and "filename" in request_data:
            simulator = Simulator()
            start_time = time()
            simulator.run_steps(request_data["run_steps"])
            print ("CPU: %4.1f steps per second" % (request_data["run_steps"]/(time() - start_time)))
            if not OPTIONS["nofile"]:
                start_time = time()
                bytes_written = simulator.dump_to_file(request_data["filename"])
                io_speed = (bytes_written/(time() - start_time))/1.0E6
                print ("IO: %4.1f MB per second average written" % io_speed)
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
            print ("Specify server port with -p <port number> or --port <port number>. Default port is 8080")
            print ("Specifying -n or --nofile option doesn't save simulation result to disk")
            sys.exit(0)
        elif opt in ('-n','--nofile'):
            OPTIONS["nofile"] = True
        elif opt in ('-p','--port'):
            OPTIONS["port"] = int(arg)
    instance = ('0.0.0.0', OPTIONS["port"])
    http_server = HTTPServer(instance, PUTHandler)
    http_server.serve_forever()

main(sys.argv[1:])
