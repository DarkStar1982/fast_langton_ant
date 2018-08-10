#!/usr/bin/python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from json import loads
import sys
import getopt

class Simulator(object):
    def __init__(self, filename):
        self.filename = filename
        self.black_cell_dict = {}
        self.machine = { "angle":90, "pos_x":0, "pos_y":0 }
        self.bounding_box = {
            "max_x":0, "offset_max_x":0,
            "max_y":0, "offset_max_y":0,
            "min_x":0, "offset_min_x":0,
            "min_y":0, "offset_min_y":0,
            "offset_x":0, "offset_y":0
        }
        self.moves = {
            0:[0,1],    # up
            90:[1,0],   # right
            180:[0,-1], # down
            270:[-1,0]} # left

    def run_steps(self, steps):
        for i in range(0,steps):
            x = self.machine["pos_x"]
            y = self.machine["pos_y"]
            # check local position and rotate counterclockwise (can go negative)
            # or clockwise (always positive) in 90 deg increments, and flip color
            if (x,y) in self.black_cell_dict:
                self.machine["angle"] = (self.machine["angle"] - 90) % 360
                del self.black_cell_dict[(x,y)]
            else:
                self.machine["angle"] = (self.machine["angle"] + 90) % 360
                self.black_cell_dict[(x,y)] = 1
            # advance one unit
            x = x + self.moves[self.machine["angle"]][0]
            y = y + self.moves[self.machine["angle"]][1]
            # update bounding box
            self.bounding_box["max_x"] = max(x, self.bounding_box["max_x"])
            self.bounding_box["max_y"] = max(y, self.bounding_box["max_y"])
            self.bounding_box["min_x"] = min(x, self.bounding_box["min_x"])
            self.bounding_box["min_y"] = min(y, self.bounding_box["min_y"])
            # update machine state
            self.machine["pos_x"] = x
            self.machine["pos_y"] = y

    def dump_to_file(self):
        # recalculate coordinate range from -x..x, -y..y to 0..X, 0..Y
        self.bounding_box["offset_x"] = 0 - self.bounding_box["min_x"]
        self.bounding_box["offset_y"] = 0 - self.bounding_box["min_y"]
        self.bounding_box["offset_min_x"] = self.bounding_box["min_x"] + self.bounding_box["offset_x"]
        self.bounding_box["offset_min_y"] = self.bounding_box["min_y"] + self.bounding_box["offset_y"]
        self.bounding_box["offset_max_x"] = self.bounding_box["max_x"] + self.bounding_box["offset_x"]
        self.bounding_box["offset_max_y"] = self.bounding_box["max_y"] + self.bounding_box["offset_y"]
        self.save_file()

    # careful - with steps=10M file size will be about 36G
    def save_file(self):
        # pass one - write down the empty field
        file = open(self.filename, "w")
        for y in range(self.bounding_box["offset_max_y"],self.bounding_box["offset_min_y"]-1, -1):
            p_line = bytearray('.' * (self.bounding_box["offset_max_x"]+1))
            file.write(p_line)
            file.write("\n")
        file.close()
        # pass two - write down the black cells
        file = open(self.filename, "r+")
        rows = (self.bounding_box["offset_max_y"])
        line_length = self.bounding_box["offset_max_x"]+2
        file_length = line_length*rows
        for item in self.black_cell_dict.keys():
            x = item[0] + self.bounding_box["offset_x"]
            y = item[1] + self.bounding_box["offset_y"]
            file.seek(file_length-y*line_length+x)
            file.write('*')
        file.close()


class PUTHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        length = self.headers['Content-Length']
        content = self.rfile.read(int(length))
        request_data = loads(content)
        if "run_steps" in request_data and "filename" in request_data:
            simulator = Simulator(request_data["filename"])
            simulator.run_steps(request_data["run_steps"])
            simulator.dump_to_file()
            self.send_response(200)
        else:
            self.send_response(400)

def run_server(port):
    instance = ('localhost', port)
    http_server = HTTPServer(instance, PUTHandler)
    http_server.serve_forever()

def main(argv):
    port = 8080
    try:
        opts, args = getopt.getopt(argv,"hp:",["help","port=",])
    except getopt.GetoptError:
        print ('server.py --help')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print "Specify server port with -p <port number> or --port <port number>"
            sys.exit(0)
        elif opt in ('-p','--port'):
            port = int(arg)
    print "Running on server port %i" % port
    run_server(port)

main(sys.argv[1:])
