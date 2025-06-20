
filename = "C:/Users/61415/PycharmProjects/SlitherCabinet/SlitherCabinet/meshesOBJ/floor_base.obj"
new_filename = "C:/Users/61415/PycharmProjects/SlitherCabinet/SlitherCabinet/meshesOBJ/floor_base_parametric.obj"

new_lines = []

with open(filename, "r") as obj_file:
    line_obj_file = obj_file.readline()
    while line_obj_file:

        if line_obj_file[:2] == "v ":
            vx, vy, vz = [value for value in line_obj_file[2:].split()]

            # x axis
            if -8 <= float(vx) < 0.0:
                vx = "left_gable_thickness+" + str(round(float(vx), 6))
            elif float(vx) == 0.0:
                vx = "left_gable_thickness"
            elif float(vx) == 300:
                vx = "width-right_gable_thickness"
            elif 300 < float(vx):
                vx = "width-right_gable_thickness+" + str(round(float(vx) - 300.0, 6))
            else:
                print("x no range")

            # y-axis
                # front edge
            if 0.0 == float(vy):
                vy = "base_edge_thickness"
                # tenon front
            elif 65.0 <= float(vy) <= 72.0:
                vy = vy
                # tenon rear
            elif 228.0 <= float(vy) <= 235.0:
                vy = "depth-back_thickness-" + str(round(300 - float(vy), 6))
            elif 300 == float(vy):
                vy = "depth-back_thickness"
            else:
                print("y no range")

            # z axis
                # bottom
            if 0.0 == float(vz):
                vz = vz
            elif 8.0 == float(vz):
                vz = "base_thickness-8"
                # top edge
            elif 16 == float(vz):
                vz = "base_thickness"
                # not accounted for
            else:
                print("z no range")



            new_lines.append("v " + vx.ljust(40) + " "
                                  + vy.ljust(50) + " "
                                  + vz.ljust(40) + " "
                                  + "\n")


        else:
            new_lines.append(line_obj_file)

        line_obj_file = obj_file.readline()

with open(new_filename, "w") as obj_parametric_file:
    for lines in new_lines:
        obj_parametric_file.writelines(lines)

