
filename = "C:/Users/61415/PycharmProjects/SlitherCabinet/SlitherCabinet/meshesOBJ/right_gable.obj"
new_filename = "C:/Users/61415/PycharmProjects/SlitherCabinet/SlitherCabinet/meshesOBJ/right_gable_parametric.obj"

new_lines = []

with open(filename, "r") as obj_file:
    line_obj_file = obj_file.readline()
    while line_obj_file:

        if line_obj_file[:2] == "v ":
            vx, vy, vz = [value for value in line_obj_file[2:].split()]
            if float(vz) <= float(20):
                print(vz)
                vz = 16 - float(vz)
                vz = round(vz, 6)
                new_lines.append("v " + "width-cth+" + vx + " "
                                      + vy + " "
                                      + "cth-" + str(vz) + " "
                                      + "\n")
            else:
                new_lines.append("v " + "width-cth+" + vx + " "
                                      + vy + " "
                                      + vz + " "
                                      + "\n")

        else:
            new_lines.append(line_obj_file)

        line_obj_file = obj_file.readline()

with open(new_filename, "w") as obj_parametric_file:
    for lines in new_lines:
        obj_parametric_file.writelines(lines)

