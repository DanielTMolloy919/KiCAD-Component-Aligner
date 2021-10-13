#!/usr/bin/python

import os
import sys

link = '' # relative path to the sketch file

comp_list = []
wire_list = []
connection_list = []
label_list = []
noconnect_list = []

# Creates arrays of line positions, for each component that needs to be fixed
with open(link, 'rt') as f: 
    for num, line in enumerate(f, 1):
        if '$Comp' in line:
            comp_list.append(num)
        if 'Wire ' in line:
            wire_list.append(num)
        if 'Connection ' in line:
            connection_list.append(num)
        if 'Text GLabel ' in line:
            label_list.append(num)
        if 'NoConn ' in line:
            noconnect_list.append(num)



    comp_list = [x+3 for x in comp_list]
    wire_list = [x+1 for x in wire_list]

update_list = []

num = 0

count = 0;

# Go line by line through the file, when the program reaches a line in one of the above arrays,
# the coordinates of the component are rewritten to the nearest 50px, according to the format of each component
# the rewritten line and line number is then added to the update_list

with open(link, 'rt') as f:
    for num, line in enumerate(f, 1): 
        if any(x == num for x in comp_list): # updating general components
            temp_line = line[2:]
            coords_dict = temp_line.split()
            new_string = 'P'
            for y in coords_dict:
                new_coordinate = 50 * round(int(y)/50)
                new_string += ' '
                new_string += str(new_coordinate)
            
            new_string += '\n'
            update_dict = [num - 1, new_string]

            update_list.append(update_dict)

        if any(z == num for z in wire_list): # updating wires
            count += 1
            #print(count)
            temp_line = line[1:]
            coords_dict = temp_line.split()
            new_string = '  '
            for y in coords_dict:
                new_coordinate = 50 * round(int(y)/50)
                new_string += str(new_coordinate)
                new_string += ' '
            
            new_string = new_string[:-1]
            new_string += '\n'

            update_dict = [num -1, new_string]

            update_list.append(update_dict)
        if any(h == num for h in connection_list): # updating wire-component connections
            coords_dict = line.split()
            coords_dict = coords_dict[2:]

            new_string = 'Connection ~'
            for y in coords_dict:
                new_string += ' '
                new_coordinate = 50 * round(int(y)/50)
                new_string += str(new_coordinate)
            
            new_string += '\n'

            update_dict = [num -1, new_string]

            update_list.append(update_dict)
        if any(i == num for i in label_list): # updating connection labels
            split_line = line.split()
            coords_dict = split_line[2:4]
            end_string = " ".join(line.split(" ", 4)[4:])

            new_string = 'Text GLabel'
            for y in coords_dict:
                new_string += ' '
                new_coordinate = 50 * round(int(y)/50)
                new_string += str(new_coordinate)
            
            new_string = new_string + ' ' + end_string

            update_dict = [num -1, new_string]

            update_list.append(update_dict)
        if any(j == num for j in noconnect_list): # updating no-connect tags
            coords_dict = line.split()
            coords_dict = coords_dict[2:]

            new_string = 'NoConn ~'
            for y in coords_dict:
                new_string += ' '
                new_coordinate = 50 * round(int(y)/50)
                new_string += str(new_coordinate)
            
            new_string += '\n'

            update_dict = [num -1, new_string]

            update_list.append(update_dict)

imported_file = []

with open(link, 'rt') as f:
    imported_file = f.readlines()

for n in update_list: # rewriting the schematic file with the list of updates
    imported_file[n[0]] = n[1]

print(imported_file)

with open(link, 'w') as f:
    f.writelines(imported_file)