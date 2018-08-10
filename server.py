#!/usr/bin/python

black_cells = []

bounding_box = {
    "max_x":0,
    "max_y":0,
    "min_x":0,
    "min_y":0
}

machine = {
    "angle":90,
    "pos_x":0,
    "pos_y":0
}


def dump_to_file():
    # calculate coordinate offsets >to 0.0
    offset_x = 0 - bounding_box["min_x"]
    offset_y = 0 - bounding_box["min_y"]
    bounding_box["min_x"] = bounding_box["min_x"] + offset_x
    bounding_box["min_y"] = bounding_box["min_y"] + offset_y
    bounding_box["max_x"] = bounding_box["max_x"] + offset_x
    bounding_box["max_y"] = bounding_box["max_y"] + offset_y
    print bounding_box
    # print black cells line by line
    for x in


def flip_color(x, y):
    # if the coordinate pair is in black cell list, remove it from black cells
    # if the coordinates pair not in black cell list, add it to black cells.
    if [x,y] in black_cells:
        black_cells.remove([x,y])
    else:
        black_cells.append([x,y])

def move_machine():
    global max_x
    global max_y
    global min_x
    global min_y
    if machine["angle"] == 0:
        machine["pos_y"] = machine["pos_y"] + 1
    if machine["angle"] == 90:
        machine["pos_x"] = machine["pos_x"] + 1
    if machine["angle"] == 180:
        machine["pos_y"] = machine["pos_y"] - 1
    if machine["angle"] == 270:
        machine["pos_x"] = machine["pos_x"] - 1
    # update ranges
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
        if [machine["pos_x"],machine["pos_y"]] in black_cells:
            # rotate counterclockwise > can go negative
            machine["angle"] = (machine["angle"] - 90) % 360
        else:
            # rotate clockwise > always positive increments
            machine["angle"] = (machine["angle"] + 90) % 360
        #
        flip_color(machine["pos_x"],machine["pos_y"])
        # advance once
        move_machine()

def main():
    step(5000)
    print machine
    print len(black_cells)
    print bounding_box
    dump_to_file()

main()
