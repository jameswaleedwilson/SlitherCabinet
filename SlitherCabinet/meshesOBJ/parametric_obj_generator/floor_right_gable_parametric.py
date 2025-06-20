
filename = "C:/Users/61415/PycharmProjects/SlitherCabinet/SlitherCabinet/meshesOBJ/floor_right_gable.obj"
new_filename = "C:/Users/61415/PycharmProjects/SlitherCabinet/SlitherCabinet/meshesOBJ/floor_right_gable_parametric.obj"

new_lines = []

with open(filename, "r") as obj_file:
    line_obj_file = obj_file.readline()
    while line_obj_file:

        if line_obj_file[:2] == "v ":
            vx, vy, vz = [value for value in line_obj_file[2:].split()]

            # x axis
            if float(vx) <= 0.0:
                vx = "width-right_gable_thickness"
            elif 0 < float(vx) < 16:
                vx = "width-right_gable_thickness+" + vx
            elif 16 <= float(vx):
                vx = "width"
            else:
                print("x no range")

            # y-axis
                # front edge
            if 0.0 == float(vy):
                vy = "right_gable_edge_thickness"
                # bottom and rail mortise front
            elif 0.0 < float(vy) <= 64.0:
                vy = vy
                # rail mortise rear
            elif 64.0 < float(vy) <= 85.0:
                vy = "rail_depth-" + str(round(100 - float(vy), 6))
                # bottom mortise rear
            elif 216 <= float(vy) <= 244:
                vy = "depth-back_thickness-" + str(round(300 - 16 - float(vy), 6))
                # rear mortise
            elif float(vy) == 284:
                vy = "depth-back_thickness"
            elif 284 < float(vy) < 300:
                vy = "depth-back_thickness+" + str(round(16 - (300- float(vy)), 6))
            elif 300 == float(vy):
                vy = "depth"
            else:
                print("y no range")

            # z axis
                # bottom
            if 0.0 == float(vz):
                vz = "right_gable_edge_thickness"
            elif 0.0 < float(vz) < 16.0:
                vz = "base_thickness-" + str(round(16.0 - float(vz), 6))
            elif 60.0 <= float(vz) <= 68.0:
                vz = vz
            elif float(vz) == 16.0:
                vz = "base_thickness"
            elif 232 <= float(vz) <= 240:
                vz = "height-" + str(round(300 - float(vz), 6))
            elif 284 == float(vz):
                vz = "height-rail_thickness"
                # rail
            elif 284 < float(vz) < 300:
                vz = "height-rail_thickness+" + str(round(16 - (300- float(vz)), 6))
                # top edge
            elif 300 == float(vz):
                vz = "height"
                # not accounted for
            else:
                print("z no range")



            new_lines.append("v " + vx.ljust(40) + " "
                                  + vy.ljust(40) + " "
                                  + vz.ljust(40) + " "
                                  + "\n")


        else:
            new_lines.append(line_obj_file)

        line_obj_file = obj_file.readline()

with open(new_filename, "w") as obj_parametric_file:
    for lines in new_lines:
        obj_parametric_file.writelines(lines)

