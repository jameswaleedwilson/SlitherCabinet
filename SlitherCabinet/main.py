# Operating system
import sys
# Python packages
"""import module_name:
   This statement imports the entire module. To access items from the module, 
   you need to use the module name as a prefix (e.g., module_name.item_name)."""
from PyQt5.QtCore import QTimer, Qt
"""from module_name import item_name:
   This statement imports specific items directly into the current namespace. 
   You can then access these items without the module name prefix (e.g., item_name)."""
# Local modules
from modules.animated_splash_screen import AnimatedSplashScreen
from modules.Camera import Camera
from modules.CompileShader import *
from modules.Light import *
from modules.LoadObject import *
from modules.MainWindow import *

class MainApp(MainWindow):

    def __init__(self):
        super().__init__()
        """Class variables"""
        self.axes_center = None
        self.axes_x = None
        self.axes_y = None
        self.axes_z = None
        self.background_color = (45.0 / 255.0, 45.0 / 255.0, 45.0 / 255.0, 1.0)
        self.camera = None
        self.current_pixel = None
        self.current_pixel_color = None
        self.depth_texture = None
        self.FBO = None
        self.grid = None
        self.lights = []
        self.mouse_x = 0
        self.mouse_y = 0
        self.pick_texture = None
        self.program_id = None
        self.shader_geometry = None
        self.shader_textured = None
        self.switcher_loc = None
        self.real_time_mouse_x = 0
        self.real_time_mouse_y = 0
        self.zoom = 50

        """50 frames per second openGL rendering"""
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.opengl_loop)
        self.timer.start(20)

    def setup_ui(self):
        # get initial openGL widget size here
        self.openGLWidget.initializeGL = self.initialise_gl
        self.openGLWidget.paintGL = self.render_gl
        self.openGLWidget.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.openGLWidget.setMouseTracking(True)
        # InstallEventFilter in openGLWidget
        self.openGLWidget.installEventFilter(self)
        # Preset openGLWidget cursor to cross-hairs
        self.openGLWidget.setCursor(Qt.CursorShape.CrossCursor)
        # Preset view to fixed isometric eye at -x,-y,+z
        self.three_d_function()

    def initialise_gl(self):
        # Enable depth testing
        glEnable(GL_DEPTH_TEST)
        # Enable blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # Initialize shaders
        self.shader_textured = CompileShader("shaders/textured.vert", "shaders/textured.frag")
        self.shader_geometry = CompileShader("shaders/geometry.vert",
                                             "shaders/geometry.frag",
                                             "shaders/geometry.geom")
        # Initialize program objects
        self.axes_center = LoadObject("meshesOBJ/axes_center.obj", "textures/yellow.png",
                                      shader=self.shader_textured)
        self.axes_x = LoadObject("meshesOBJ/axes_x.obj", "textures/red.png",
                                 shader=self.shader_textured)
        self.axes_y = LoadObject("meshesOBJ/axes_y.obj", "textures/green.png",
                                 shader=self.shader_textured)
        self.axes_z = LoadObject("meshesOBJ/axes_z.obj", "textures/blue.png",
                                 shader=self.shader_textured)
        self.grid = LoadObject("meshesOBJ/plate.obj", "textures/grid_solid_bg.png",
                               location=pygame.Vector3(0, 0, -0.01),
                               image_back="textures/grid_transparent_bg.png",
                               shader=self.shader_textured)
        # Initialize lights
        self.lights.append(Light(pygame.Vector3(-300, -150, 1000), pygame.Vector3(1, 1, 1), 0,
                                 move_with_camera=True))
        """
        # Create the Custom FBO
        self.FBO = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)

        # Create picking texture and a frame buffer object
        self.pick_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.pick_texture)
        # this can be larger will only write what is available ?????
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 2000, 2000, 0, GL_RGB, GL_FLOAT, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.pick_texture, 0)

        # Create the texture object for the depth buffer
        self.depth_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.depth_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, 2000, 2000, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depth_texture, 0)

        # Verify that the FBO is correct
        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
            print("FB error, status: ", status)
            exit(1)
        # Restore the default frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, 0)"""

    def render_gl(self):

        self.camera = Camera(self.openGLWidget.width(), self.openGLWidget.height())

        # START DRAW TO DEFAULT FBO
        # set default background color -> '*' unpacks tuple
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.axes_center.draw_default_fbo(self.camera, self.lights, self.zoom, self.roll, self.pitch, self.yaw,
                                          self.view,
                                          object_color_identifier_default_fbo=(1, 0, 0),
                                          current_pixel_color=self.current_pixel_color)
        self.axes_x.draw_default_fbo(self.camera, self.lights, self.zoom, self.roll, self.pitch, self.yaw,
                                     self.view,
                                     object_color_identifier_default_fbo=(1, 0, 0),
                                     current_pixel_color=self.current_pixel_color)
        self.axes_y.draw_default_fbo(self.camera, self.lights, self.zoom, self.roll, self.pitch, self.yaw,
                                     self.view,
                                     object_color_identifier_default_fbo=(1, 0, 0),
                                     current_pixel_color=self.current_pixel_color)
        self.axes_z.draw_default_fbo(self.camera, self.lights, self.zoom, self.roll, self.pitch, self.yaw,
                                     self.view,
                                     object_color_identifier_default_fbo=(1, 0, 0),
                                     current_pixel_color=self.current_pixel_color)

        self.grid.draw_default_fbo(self.camera, self.lights, self.zoom, self.roll, self.pitch, self.yaw, self.view,
                                   object_color_identifier_default_fbo=(255, 0, 0),
                                   current_pixel_color=self.current_pixel_color)
        # START USER OBJECTS

        # END USER OBJECTS

        # END DRAW TO DEFAULT FBO
        """
        # START DRAW TO CUSTOM FBO
        # bind Custom FBO -> comment out below line to view the Custom FBO
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        # set custom background color to black
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # START USER OBJECTS
        # self.hemera.draw_custom_fbo(self.camera, self.zoom, self.roll, self.pitch, self.yaw, self.view,
        #                             object_color_identifier_custom_fbo=(2, 255, 0))
        # END USER OBJECTS

        # Unbind Custom FBO
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        # END DRAW TO CUSTOM FBO

        # START READ PIXELS
        # bind Custom FBO
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        current_pixel_color = glReadPixels(self.real_time_mouse_x, self.real_time_mouse_y, 1, 1, GL_RGB,
                                           GL_UNSIGNED_BYTE)
        self.current_pixel_color = (current_pixel_color[0], current_pixel_color[1], current_pixel_color[2])
        # print(self.current_pixel_color)
        # unbind Custom FBO
        glBindFramebuffer(GL_FRAMEBUFFER, 0)"""
        # END READ PIXELS

    def opengl_loop(self):
        self.openGLWidget.update()


"""1.Close AnimatedSplashScreen() and open MainWindow()"""
def execute_functions():
    window.show()
    animated_splash_screen.finish(window)


"""Run Main App"""
if __name__ == '__main__':
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=2'])

    # Initialise AnimatedSplashScreen()
    animated_splash_screen = AnimatedSplashScreen()
    animated_splash_screen.show()
    # Allows the splash screen to be displayed immediately
    app.processEvents()

    window = MainApp()
    window.setup_ui()

    # 2.Close AnimatedSplashScreen() and open MainWindow()
    timer = QTimer()
    timer.timeout.connect(execute_functions)
    timer.start(11546)

    #window.show()
    app.exec()
