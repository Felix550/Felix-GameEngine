import pygame
import Types
import time
import ctypes


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
        self.data[key] = value

    def get_data(self, key):
        return self.data[key]

    def colliding(self, other: 'Actor'):
        # --- Rettangolo vs Rettangolo ---
        if self.shape_type == Types.ShapeType.RECTANGLE and other.shape_type == Types.ShapeType.RECTANGLE:
            size1 = self.data["size"] or Types.Vector2D(1, 1)
            size2 = other.data["size"] or Types.Vector2D(1, 1)
            align1 = self.data["align"] or Types.Align.CORNER
            align2 = other.data["align"] or Types.Align.CORNER

            rect1 = pygame.Rect(
                self.position.x - (0 if align1 == Types.Align.CORNER else size1.x / 2),
                self.position.y - (0 if align1 == Types.Align.CORNER else size1.y / 2),
                size1.x, size1.y
            )
            rect2 = pygame.Rect(
                other.position.x - (0 if align2 == Types.Align.CORNER else size2.x / 2),
                other.position.y - (0 if align2 == Types.Align.CORNER else size2.y / 2),
                size2.x, size2.y
            )
            return rect1.colliderect(rect2)

        # --- Cerchio vs Cerchio ---
        elif self.shape_type == Types.ShapeType.CIRCLE and other.shape_type == Types.ShapeType.CIRCLE:
            r1 = (self.data["size"] or Types.Vector2D(20, 20)).x / 2
            r2 = (other.data["size"] or Types.Vector2D(20, 20)).x / 2
            dx = self.position.x - other.position.x
            dy = self.position.y - other.position.y
            return dx * dx + dy * dy <= (r1 + r2) ** 2

        # --- Rettangolo vs Cerchio ---
        elif self.shape_type == Types.ShapeType.RECTANGLE and other.shape_type == Types.ShapeType.CIRCLE:
            return self._rect_circle_collision(self, other)

        elif self.shape_type == Types.ShapeType.CIRCLE and other.shape_type == Types.ShapeType.RECTANGLE:
            return self._rect_circle_collision(other, self)

        return False

    def _rect_circle_collision(self, rect_actor, circle_actor):
        size = rect_actor.data["size"] or Types.Vector2D(1, 1)
        align = rect_actor.data["align"] or Types.Align.CORNER
        radius = (circle_actor.data["size"] or Types.Vector2D(20, 20)).x / 2

        rect_x = rect_actor.position.x - (0 if align == Types.Align.CORNER else size.x / 2)
        rect_y = rect_actor.position.y - (0 if align == Types.Align.CORNER else size.y / 2)
        rect = pygame.Rect(rect_x, rect_y, size.x, size.y)

        cx, cy = circle_actor.position.x, circle_actor.position.y
        closest_x = max(rect.left, min(cx, rect.right))
        closest_y = max(rect.top, min(cy, rect.bottom))

        dx = cx - closest_x
        dy = cy - closest_y
        return dx * dx + dy * dy <= radius ** 2


class Canvas:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def fill(self, color: Types.Color):
        self.screen.fill(color)

    def draw(self, actor: Actor):
        if actor.shape_type == Types.ShapeType.RECTANGLE:
            size = actor.data["size"] or Types.Vector2D(1, 1)
            align = actor.data["align"] or Types.Align.CORNER
            X = actor.position.x - (0 if align == Types.Align.CORNER else size.x / 2)
            Y = actor.position.y - (0 if align == Types.Align.CORNER else size.y / 2)
            pygame.draw.rect(self.screen, actor.data["color"] or Types.Color(0, 0, 0),
                             pygame.Rect(X, Y, size.x, size.y))

        elif actor.shape_type == Types.ShapeType.CIRCLE:
            size = actor.data["size"] or Types.Vector2D(50, 50)
            pygame.draw.circle(self.screen, actor.data["color"] or Types.Color(0, 0, 0),
                               actor.position, size.x / 2)

        elif actor.shape_type == Types.ShapeType.SPRITE:
            size = actor.data["size"] or Types.Vector2D(1, 1)
            px = actor.position.x - size.x / 2
            py = actor.position.y - size.y / 2
            sx, sy = size.x, size.y

            pygame.draw.ellipse(self.screen, (255, 255, 0), (px, py, sx, sy))
            pygame.draw.ellipse(self.screen, (0, 0, 0),
                                (px + sx * 0.25 - sx * 0.1, py + sy * 0.25 - sy * 0.1, sx * 0.2, sy * 0.2))
            pygame.draw.ellipse(self.screen, (0, 0, 0),
                                (px + sx * 0.75 - sx * 0.1, py + sy * 0.25 - sy * 0.1, sx * 0.2, sy * 0.2))
            pygame.draw.arc(self.screen, (0, 0, 0),
                            (px + sx * 0.25, py + sy * 0.5, sx * 0.5, sy * 0.3), 3.14, 0, 3)


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
        ctypes.windll.user32.ShowWindow(self._console_handle, 5)

    def hide_console(self):
        ctypes.windll.user32.ShowWindow(self._console_handle, 0)


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
        return Types.Vector2D(x, y)

    def set_pos(self, newPos):
        self.mouse.set_pos((newPos.x, newPos.y))

    def GetButton(self, button: int) -> bool:
        return self.buttons[button]

    def GetButtonDown(self, button: int) -> bool:
        return self.buttons[button] and not self.prev_buttons[button]

    def GetButtonUp(self, button: int) -> bool:
        return not self.buttons[button] and self.prev_buttons[button]

    def _end_frame(self):
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
        print(f"[{time.strftime('%H:%M:%S')}] {text}")
