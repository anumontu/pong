import pygame


class Window:
    """
    Window
    """

    def __init__(self, size: tuple, name: str, fps: int = 120, resizable: bool = True):
        """
        Initialize window
        :param size: Window size
        :param name: Name
        :param fps: FPS
        :param resizable: Is the window resizeable ?
        """
        self.resizable = resizable
        self.size = size
        self.width = size[0]
        self.height = size[1]
        if self.resizable:
            self.window = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        else:
            self.window = pygame.display.set_mode(self.size)
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.fps = fps

    def update(self):
        """
        Event Updates
        :return: Events list
        """
        if self.is_open():
            pygame.display.flip()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                elif event.type == pygame.VIDEORESIZE:
                    self.resize(event.size)
            self.clock.tick(self.fps)
            return events

    def blit(self, surface: pygame.Surface):
        """
        Draw with updated size
        :param surface: Surface object
        """
        if self.is_open():
            self.window.blit(surface, (0, 0))

    def smooth_scaled_blit(self, surface):
        """
        Scale a surface to an arbitrary size smoothly
        :param surface: Surface object
        """
        pygame.transform.smoothscale(surface, (self.width, self.height), self.window)

    @staticmethod
    def is_open():
        """
        Returns True if the display module has been initialized
        :return: display module has been initialized or not ?
        """
        return pygame.display.get_init()

    def resize(self, new_size):
        """
        Resize window
        :param new_size: New window size
        """
        if self.is_open():
            image = self.window.copy()
            self.size = new_size
            self.width = self.size[0]
            self.height = self.size[1]
            if self.resizable:
                self.window = pygame.display.set_mode(self.size, pygame.RESIZABLE)
            else:
                self.window = pygame.display.set_mode(self.size)
            self.blit(pygame.transform.scale(image, self.size))
