import pygame
from OpenGL.GL import *


class LoadTexture:
    def __init__(self, image_filename=None):
        self.image = None
        self.id = glGenTextures(1)
        if image_filename is not None:
            self.image = pygame.image.load(image_filename)
            self.load()

    def load(self):
        image_width = self.image.get_width()
        image_height = self.image.get_height()

        pixel_data = pygame.image.tostring(self.image, "RGBA", True)
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixel_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
