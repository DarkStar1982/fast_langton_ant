#!/usr/bin/python

black_cells = []
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
}

machine = {
    "angle":90,
    "pos_x":0,
    "pos_y":0
}

def get_black_cells(y_pos, p_line):
    offset_x = 0 - bounding_box["min_x"]
    offset_y = 0 - bounding_box["min_y"]
    y = y_pos - offset_y
    # print y
    for x_pos in range(bounding_box["offset_min_x"],bounding_box["offset_max_x"]+1):
        x = x_pos - offset_x
        if [x,y] in black_cells:
            p_line[x+offset_x] = ('*')
    return p_line

# recalculate coordinates
def dump_to_file():
    offset_x = 0 - bounding_box["min_x"]
    offset_y = 0 - bounding_box["min_y"]
    bounding_box["offset_min_x"] = bounding_box["min_x"] + offset_x
    bounding_box["offset_min_y"] = bounding_box["min_y"] + offset_y
    bounding_box["offset_max_x"] = bounding_box["max_x"] + offset_x
    bounding_box["offset_max_y"] = bounding_box["max_y"] + offset_y
    for y in range(bounding_box["offset_max_y"],bounding_box["offset_min_y"]-1, -1):
        line_x = bytearray('.' * (bounding_box["offset_max_x"]+1))
        line_x = get_black_cells(y,line_x)
        print line_x # or write to file

# if the coordinate pair is in black cell list, remove it from black cells
# if the coordinates pair not in black cell list, add it to black cells.
def flip_color(x, y):
    if [x,y] in black_cells:
        black_cells.remove([x,y])
    else:
        black_cells.append([x,y])
        # black_cell_dict[(x,y)] = 1

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
        if [machine["pos_x"],machine["pos_y"]] in black_cells:
            # rotate counterclockwise > can go negative
            machine["angle"] = (machine["angle"] - 90) % 360
        else:
            # rotate clockwise > always positive increments
            machine["angle"] = (machine["angle"] + 90) % 360
        flip_color(machine["pos_x"],machine["pos_y"])
        # advance once
        move_machine()

def main():
    step(1)
    #print machine
    #print black_cells
    #print bounding_box
    # print '#Life 1.05'
    dump_to_file()

main()
