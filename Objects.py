import pygame
import Types
import time
import ctypes
import sys


class Actor:
    def __init__(self, position: Types.Vector2D, shape_type: Types.ShapeType, data: dict):
        self.position = position
        self.shape_type = shape_type
        self.data = data

    def move(self, deltaPosition: Types.Vector2D):
        self.position += deltaPosition

    def set_pos(self, newPosition: Types.Vector2D):
        self.position = newPosition

    def get_pos(self):
        return self.position

    def change_data(self, key, value):
        if key in self.data:
            self.data[key] = value
        else:
            raise KeyError(f"'{key}' is not a valid property for this Actor.")

    def get_data(self, key):
        if key in self.data:
            return self.data[key]
        else:
            raise KeyError(f"'{key}' is not a valid property for this Actor.")


class Canvas:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def fill(self, color: Types.Color):
        self.screen.fill(color)

    def draw(self, actor: Actor):
        if actor.shape_type == Types.ShapeType.RECTANGLE:
            size = actor.data["size"] or Types.Vector2D(1, 1)
            align = actor.data["align"] or Types.Align.CORNER

            X = actor.position.x - \
                (0 if align == Types.Align.CORNER else size.x / 2)
            Y = actor.position.y - \
                (0 if align == Types.Align.CORNER else size.y / 2)
            pygame.draw.rect(surface=self.screen,
                             color=actor.data["color"] or Types.Color(0, 0, 0),
                             rect=pygame.Rect(X, Y,
                                              size.x, size.y)
                             )
        elif actor.shape_type == Types.ShapeType.CIRCLE:
            pygame.draw.circle(surface=self.screen,
                               color=actor.data["color"] or Types.Color(
                                   0, 0, 0),
                               center=actor.position,
                               radius=actor.data["radius"] or 50
                               )
        elif actor.shape_type == Types.ShapeType.SPRITE:
            size = actor.data["size"] or Types.Vector2D(1, 1)
            # offset per centraggio
            px = actor.position.x - size.x / 2
            py = actor.position.y - size.y / 2
            sx, sy = size.x, size.y

            # faccina
            pygame.draw.ellipse(self.screen, (255, 255, 0), (px, py, sx, sy))

            # occhi (relativi alla dimensione della faccina)
            pygame.draw.ellipse(self.screen, (0, 0, 0),
                                (px + sx*0.25 - sx*0.1, py + sy*0.25 - sy*0.1, sx*0.2, sy*0.2))
            pygame.draw.ellipse(self.screen, (0, 0, 0),
                                (px + sx*0.75 - sx*0.1, py + sy*0.25 - sy*0.1, sx*0.2, sy*0.2))

            # bocca (arco adattato alla dimensione)
            pygame.draw.arc(self.screen, (0, 0, 0),
                            (px + sx*0.25, py + sy*0.5, sx*0.5, sy*0.3),
                            3.14, 0, 3)


class Window:
    def __init__(self, FPS):
        self.display = pygame.display
        self._console_handle = ctypes.windll.kernel32.GetConsoleWindow()
        self.FPS = FPS

    def set_title(self, title: str):
        self.display.set_caption(title)

    def get_title(self):
        return self.display.get_caption()[0]

    def set_size(self, size: Types.Vector2D):
        self.display.set_mode(size)

    def get_size(self):
        w, h = self.display.get_window_size()
        return Types.Vector2D(w, h)

    def set_target_fps(self, targetFPS):
        self.FPS = targetFPS

    def get_target_fps(self):
        return self.FPS

    def toggle_fullscreen(self):
        self.display.toggle_fullscreen()

    def show_console(self):
        """Mostra la console."""
        ctypes.windll.user32.ShowWindow(self._console_handle, 5)  # 5 = SW_SHOW

    def hide_console(self):
        """Nasconde la console."""
        ctypes.windll.user32.ShowWindow(self._console_handle, 0)  # 0 = SW_HIDE


class Screen:
    def __init__(self):
        self.info = pygame.display.Info()

    def get_size(self):
        return Types.Vector2D(self.info.current_w, self.info.current_h)


class Mouse:
    def __init__(self):
        self.mouse = pygame.mouse
        self.prev_buttons = self.mouse.get_pressed()
        self.buttons = self.prev_buttons

    def _update(self):
        self.buttons = self.mouse.get_pressed()

    def get_pos(self):
        x, y = self.mouse.get_pos()
        # supponendo che Types.Vector2D sia la tua classe vettore
        return Types.Vector2D(x, y)

    def set_pos(self, newPos):
        self.mouse.set_pos((newPos.x, newPos.y))

    def GetButton(self, button: int) -> bool:
        """True se il pulsante è tenuto premuto."""
        return self.buttons[button]

    def GetButtonDown(self, button: int) -> bool:
        """True solo nel frame in cui il pulsante viene premuto."""
        return self.buttons[button] and not self.prev_buttons[button]

    def GetButtonUp(self, button: int) -> bool:
        """True solo nel frame in cui il pulsante viene rilasciato."""
        return not self.buttons[button] and self.prev_buttons[button]

    def _end_frame(self):
        """Da chiamare a fine frame per aggiornare lo stato precedente."""
        self.prev_buttons = self.buttons


class Input:
    def __init__(self):
        self.key = pygame.key
        self.prev_keys = pygame.key.get_pressed()
        self.keys = self.prev_keys

    def _update(self):
        self.keys = self.key.get_pressed()

    def GetKey(self, key: int) -> bool:
        return self.keys[key]

    def GetKeyDown(self, key: int) -> bool:
        return self.keys[key] and not self.prev_keys[key]

    def GetKeyUp(self, key: int) -> bool:
        return not self.keys[key] and self.prev_keys[key]

    def _end_frame(self):
        self.prev_keys = self.keys


class Debug:
    def __init__(self):
        pass

    def log(self, text):
        print(f"[{time.strftime("%H:%M:%S")}] {text}")
