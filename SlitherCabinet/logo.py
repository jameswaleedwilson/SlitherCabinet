import re

current_line_count = 0

# open the sample gcode used
gcode = open("gcode/sliverTree.gcode")
# read the content of the gcode opened
data = gcode.readlines()
# print(data)
number_gcode_rows = len(data)
# print(number_gcode_rows)

file1 = open('sliver.scr', 'r+')
file1.truncate(0)

file1 = open('sliver.scr', 'a')
file1.writelines('_MULTIPLE _LINE\n')

extrude1 = 1.0
extrude2 = 0.0
new_move = False

x1 = 0.0
y1 = 0.0
z1 = 0.0
x2 = 0.0
y2 = 0.0
z2 = 0.0

while current_line_count < number_gcode_rows:
    current_line = data[current_line_count]
    # remove \n
    current_line = current_line.strip()
    # remove double white space
    current_line = re.sub(' {3}', ' ', current_line)
    current_line = re.sub(' {2}', ' ', current_line)

    if current_line[:3] == "G1 " or current_line[:3] == "G92":

        for i in current_line.split(' '):
            if i[0] == 'X':
                if current_line_count > 0:
                    x2 = float(i[1:])
                else:
                    x1 = float(i[1:])
                new_move = True
            if i[0] == 'Y':
                if current_line_count > 0:
                    y2 = float(i[1:])
                else:
                    y1 = float(i[1:])
                new_move = True
            if i[0] == 'Z':
                if current_line_count > 0:
                    z2 = float(i[1:])
                else:
                    z1 = float(i[1:])
                new_move = True
            if i[0] == 'E':
                if current_line_count > 0:
                    extrude2 = float(i[1:])
                else:
                    extrude1 = float(i[1:])

        if z1.is_integer() and z2.is_integer() and new_move:
            file1.writelines(str(x1) + ',' + str(y1) + ',' + str(z1) + '\n')
            print(str(x1) + ',' + str(y1) + ',' + str(z1) + ',' + str(extrude1))
            file1.writelines(str(x2) + ',' + str(y2) + ',' + str(z2) + '\n')
            print(str(x2) + ',' + str(y2) + ',' + str(z2) + ',' + str(extrude2) + '\n')

        new_move = False

    x1 = x2
    y1 = y2
    z1 = z2
    extrude1 = extrude2

    current_line_count += 1

file1.close()
