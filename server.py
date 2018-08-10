#!/usr/bin/python
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

black_cell_dict = {
}

bounding_box = {
    "max_x":0,
    "max_y":0,
    "min_x":0,
    "min_y":0,
    "offset_max_x":0,
    "offset_max_y":0,
    "offset_min_x":0,
    "offset_min_y":0,
    "offset_x":0,
    "offset_y":0
}

machine = {
    "angle":90,
    "pos_x":0,
    "pos_y":0
}

def get_black_cells(y):
    p_line = bytearray('.' * (bounding_box["offset_max_x"]+1))
    # print y
    for x in range(bounding_box["min_x"],bounding_box["max_x"]+1):
        if (x,y) in black_cell_dict:
            p_line[x+bounding_box["offset_x"]] = ('*')
    return p_line

# recalculate coordinate range from -x..x, -y..y to 0..X, 0..Y
def update_bounding_box():
    bounding_box["offset_x"] = 0 - bounding_box["min_x"]
    bounding_box["offset_y"] = 0 - bounding_box["min_y"]
    bounding_box["offset_min_x"] = bounding_box["min_x"] + bounding_box["offset_x"]
    bounding_box["offset_min_y"] = bounding_box["min_y"] + bounding_box["offset_y"]
    bounding_box["offset_max_x"] = bounding_box["max_x"] + bounding_box["offset_x"]
    bounding_box["offset_max_y"] = bounding_box["max_y"] + bounding_box["offset_y"]

# print to stdout or write to file
def dump_to_file():
    for y in range(bounding_box["offset_max_y"],bounding_box["offset_min_y"]-1, -1):
        line_x = get_black_cells(y-bounding_box["offset_y"])
        print line_x

# if the coordinate pair is in black cell list, remove it from black cells
# if the coordinates pair not in black cell list, add it to black cells.
def flip_color(x, y):
    if (x,y) in black_cell_dict:
        del black_cell_dict[(x,y)]
    else:
        black_cell_dict[(x,y)] = 1

# move the machine and update bounding box
def move_machine():
    if machine["angle"] == 0:
        machine["pos_y"] = machine["pos_y"] + 1
    if machine["angle"] == 90:
        machine["pos_x"] = machine["pos_x"] + 1
    if machine["angle"] == 180:
        machine["pos_y"] = machine["pos_y"] - 1
    if machine["angle"] == 270:
        machine["pos_x"] = machine["pos_x"] - 1
    if (machine["pos_x"]>bounding_box["max_x"]):
        bounding_box["max_x"] = machine["pos_x"]
    if (machine["pos_y"]>bounding_box["max_y"]):
        bounding_box["max_y"] = machine["pos_y"]
    if (machine["pos_x"]<bounding_box["min_x"]):
        bounding_box["min_x"] = machine["pos_x"]
    if (machine["pos_y"]<bounding_box["min_y"]):
        bounding_box["min_y"] = machine["pos_y"]

def step(steps):
    #check the grid state
    for i in range(0,steps):
        # check local position
        if (machine["pos_x"],machine["pos_y"]) in black_cell_dict:
            # rotate counterclockwise > can go negative
            machine["angle"] = (machine["angle"] - 90) % 360
        else:
            # rotate clockwise > always positive increments
            machine["angle"] = (machine["angle"] + 90) % 360
        flip_color(machine["pos_x"],machine["pos_y"])
        # advance once
        move_machine()


def main():
    step(1000000000)
    #print machine
    update_bounding_box()
    #dump_to_file()
    print len(black_cell_dict)
    print bounding_box

main()
