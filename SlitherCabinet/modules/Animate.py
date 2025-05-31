import numpy as np
import pygame


class Animate:

    def __init__(self):

        self.position = pygame.Vector3(0.0, 0.0, 0.0)
        self.home = pygame.Vector3(-50, 0.0, 50)
        self.current_line_count = 0
        self.gcode, self.number_gcode_rows = self.load()

    @staticmethod
    def load():
        # open the sample gcode used
        gcode = open("gcode/teapot.gcode")
        # read the content of the gcode opened
        data = gcode.readlines()
        number_gcode_rows = len(data)
        print(number_gcode_rows)
        return data, number_gcode_rows

    def get_next_position(self):

        if self.current_line_count < self.number_gcode_rows:
            current_line = self.gcode[self.current_line_count]
            self.current_line_count += 1
            # remove \n
            current_line = current_line.strip()
            print("current_line", current_line)
            if current_line[:3] == "G1 ":
                for i in current_line.split(' '):
                    if i[0] == 'X':
                        self.position.x = float(i[1:])
                    if i[0] == 'Y':
                        self.position.y = float(i[1:])
                    if i[0] == 'Z':
                        self.position.z = float(i[1:])
            print(self.current_line_count)
            print("position", self.position)

        if self.current_line_count == self.number_gcode_rows:
            self.current_line_count += 1
            # return home
            self.position = self.home
            print('home')
            print("position", self.position)

        new_position = pygame.Vector3(self.position.x, self.position.y, self.position.z)

        return new_position
