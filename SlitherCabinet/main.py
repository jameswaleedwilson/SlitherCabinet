# Operating system
"""None"""
# Python packages
"""None"""
# Local modules
from modules.animated_splash_screen import AnimatedSplashScreen
from modules.camera import Camera
from modules.compile_shader import *
from modules.main_window import *
from modules.light import *
from modules.LoadVBO import *
from data_app.mesh_data_app import mesh_data_app
from data_user.mesh_data_user import mesh_data_user

gl_loop = 0
load_once = True


""" Main application inherits from MainWindow(QtWidgets.QMainWindow) """
class MainApp(MainWindow):

    def __init__(self):
        super().__init__()

        self.meshes_app = []
        self.meshes_user = []
        self.job_loaded = True

        self.animation = None
        self.depth_texture = None
        self.switcher_loc = None
        self.FBO1 = None
        self.pick_texture = None
        self.shader_textured = None
        self.current_pixel_color = None
        self.current_pixel = None
        self.clip_plane = None
        self.camera = None
        self.program_id = None
        self.lights = []
        self.window_settings_minimized = None
        self.window_settings_maximized = QtCore.QSettings("Slither", "maximized")

        self.mouse_x = 0
        self.mouse_y = 0
        self.real_time_mouse_x = 0
        self.real_time_mouse_y = 0

        # initial values/settings
        self.zoom = 200
        self.background_color = (45.0 / 255.0, 45.0 / 255.0, 45.0 / 255.0, 1.0)
        self.verticalSlider_glClipPlane.setValue(300)
        self.toolButton_axes.setChecked(True)
        self.toolButton_grid.setChecked(True)
        self.toolButton_CAD.setChecked(True)

        # opengl gl loop 50 Hz
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.opengl_loop)
        self.timer.start(20)

        self.test_draw = 0

    def setup_ui(self):
        # Reimplement QOpenGLWidget virtual functions as subclasses to perform the typical OpenGL tasks
        self.openGLWidget.initializeGL = self.initialise_gl
        self.openGLWidget.paintGL = self.paint_gl
        # a method used to define widget accepts keyboard focus
        self.openGLWidget.setFocusPolicy(Qt.StrongFocus)
        # a function used to control whether mouse move events (specifically, mouseMoveEvent)
        # are sent to a widget even when no mouse button is pressed
        self.openGLWidget.setMouseTracking(True)
        # installEventFilter sends the events to the eventFilter
        self.openGLWidget.installEventFilter(self)
        # preset cursor to cross-hairs
        self.openGLWidget.setCursor(Qt.CrossCursor)

        self.label_roll.setText('Roll ' + str(self.roll))
        self.label_pitch.setText('Pitch ' + str(self.pitch))
        self.label_yaw.setText('Yaw ' + str(self.yaw))
        self.label_zoom.setText('Zoom ' + str(self.zoom))
        self.axes_function(True)
        self.grid_function(True)
        self.three_d_function()

    def minimize_function(self):
        window.showMinimized()

    def maximize_function(self):
        if self.windowState() & QtCore.Qt.WindowState.WindowMaximized:
            self.restoreGeometry(self.window_settings_maximized.value("geometry"))
            self.restoreState(self.window_settings_maximized.value("windowState"))
        else:
            self.window_settings_maximized.setValue("geometry", self.saveGeometry())
            self.window_settings_maximized.setValue("windowState", self.saveState())
            window.showMaximized()

    def close_function(self):
        window.close()

    def initialise_gl(self):
        # query double buffering

        # enable depth testing
        glEnable(GL_DEPTH_TEST)
        # enable blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # initialise shaders
        self.shader_textured = CompileShader("shaders/textured.vert", "shaders/textured.frag")
        # animation
        #self.animation = Animate()

        """ initialise app objects """
        # Loop to create and store objects
        for mesh in mesh_data_app:
            obj = LoadVBO(mesh["mesh"],
                          mesh["texture_front"],
                          image_back=mesh["texture_back"],
                          shader=self.shader_textured)
            self.meshes_app.append(obj)

        # initialise lights
        self.lights.append(Light(pygame.Vector3(-300, -150, 1000), pygame.Vector3(1, 1, 1), 0,
                                 move_with_camera=True))

        # Create the Custom FBO #1
        self.FBO1 = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO1)

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
            print("Frame Buffer error, status: ", status)
            exit(1)
        # Restore the default frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, 0)

    def paint_gl(self):
        global gl_loop
        gl_loop += 1
        print(gl_loop)
        self.camera = Camera(self.openGLWidget.width(), self.openGLWidget.height())

        """ START DRAW TO DEFAULT FBO """
        # set default background color -> '*' unpacks tuple
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if gl_loop > 100:
            for obj in self.meshes_user:
                obj.draw_default_fbo(self.camera, self.lights, self.zoom, self.roll, self.pitch, self.yaw, self.view,
                                     current_pixel_color=self.current_pixel_color)

        for obj in self.meshes_app:
            obj.draw_default_fbo(self.camera, self.lights, self.zoom, self.roll, self.pitch, self.yaw, self.view)

        """ END DRAW TO DEFAULT FBO """

        """ START DRAW TO CUSTOM FBO """
        # bind Custom FBO -> comment out below line to view the Custom FBO
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO1)
        # set custom background color to black
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if gl_loop > 100:
            for obj in self.meshes_user:
                obj.draw_custom_fbo(self.camera, self.zoom, self.roll, self.pitch, self.yaw, self.view)

        # Unbind Custom FBO
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        """ END DRAW TO CUSTOM FBO """

        """ START READ PIXELS """
        # bind Custom FBO
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO1)
        current_pixel_color = glReadPixels(self.real_time_mouse_x, self.real_time_mouse_y, 1, 1, GL_RGB,
                                           GL_UNSIGNED_BYTE)
        self.current_pixel_color = (current_pixel_color[0], current_pixel_color[1], current_pixel_color[2])
        #print(self.current_pixel_color)
        # unbind Custom FBO
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        """ END READ PIXELS """

        # Update UI
        self.label_roll.setText('Roll ' + str(self.roll))
        self.label_pitch.setText('Pitch ' + str(self.pitch))
        self.label_yaw.setText('Yaw ' + str(self.yaw))
        self.label_zoom.setText('Zoom ' + str(round(self.zoom, 1)))

        # initialise new user objects
        global load_once
        if gl_loop < 10 and load_once:
            for mesh in mesh_data_user:
                obj = LoadVBO(mesh["mesh"],
                              mesh["texture_front"],
                              shader=self.shader_textured,
                              identifier=mesh["identifier"],
                              location=pygame.Vector3(mesh["location"][0], mesh["location"][1], mesh["location"][2]),
                              move_scale=pygame.Vector3(mesh["scale"][0], mesh["scale"][1], mesh["scale"][2]))
                self.meshes_user.append(obj)
            load_once = False

    def opengl_loop(self):
        # This function does not cause an immediate repaint; instead it schedules a paint event for
        # processing when Qt returns to the main event loop. This permits Qt to optimize for more
        # speed and less flicker than a call to repaint() does.
        self.openGLWidget.update()


"""1.Close AnimatedSplashScreen() and open MainWindow()"""
def switch_screens():
    window.show()
    animated_splash_screen.finish(window)


""" Run Main App """
if __name__ == '__main__':
    app = QApplication([])

    # Initialise AnimatedSplashScreen()
    animated_splash_screen = AnimatedSplashScreen()
    animated_splash_screen.show()
    # Allows the splash screen to be displayed immediately
    app.processEvents()

    window = MainApp()
    window.setup_ui()

    # 2.Close AnimatedSplashScreen() and open MainWindow()
    timer = QtCore.QTimer()
    timer.timeout.connect(switch_screens)
    timer.start(1546)

    # window.show()
    app.exec()
