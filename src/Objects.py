import pygame
import Types
import time
import ctypes
import os

class Actor:
    def __init__(self, position: Types.Vector2D, shape_type: Types.ShapeType, data: dict):
        self.position = position
        self.shape_type = shape_type
        if data is None:
            self.data = {}
        elif isinstance(data, dict):
            self.data = data
        else:
            try:
                self.data = dict(data)
            except Exception:
                self.data = {}

    def move(self, deltaPosition: Types.Vector2D):
        self.position += deltaPosition

    def set_pos(self, newPosition: Types.Vector2D):
        self.position = newPosition

    def get_pos(self):
        return self.position

    def change_data(self, key, value):
        self.data[key] = value

    def get_data(self, key, default=None):
        return self.data.get(key, default)
    
    def get_size(self):
        if self.shape_type != Types.ShapeType.TEXT:
            raise DeprecationWarning("This function is only for Text. Use get_data('size') for other shapes.")

        text = self.data.get("text", "")
        font = self.data.get("font", Types.Font("Comic Sans MS", 20))

        # cache del font pygame per evitare di ricrearlo ogni volta
        if not hasattr(font, "_pg_font"):
            font._pg_font = font._construct()

        width, height = font._pg_font.size(text)
        return Types.Vector2D(width, height)

        

    """
    def colliding(self, other: 'Actor'):
        # --- Rettangolo vs Rettangolo ---
        if self.shape_type == Types.ShapeType.RECTANGLE and other.shape_type == Types.ShapeType.RECTANGLE:
            size1 = self.data.get("size", Types.Vector2D(1, 1))
            size2 = other.data.get("size", Types.Vector2D(1, 1))
            align1 = self.data.get("align", Types.Align.CORNER)
            align2 = other.data.get("align", Types.Align.CORNER)

            rect1 = pygame.Rect(
                self.position.x -
                (0 if align1 == Types.Align.CORNER else size1.x / 2),
                self.position.y -
                (0 if align1 == Types.Align.CORNER else size1.y / 2),
                size1.x, size1.y
            )
            rect2 = pygame.Rect(
                other.position.x -
                (0 if align2 == Types.Align.CORNER else size2.x / 2),
                other.position.y -
                (0 if align2 == Types.Align.CORNER else size2.y / 2),
                size2.x, size2.y
            )
            return rect1.colliderect(rect2)

        # --- Cerchio vs Cerchio ---
        elif self.shape_type == Types.ShapeType.ELLIPSE and other.shape_type == Types.ShapeType.ELLIPSE:
            r1 = self.data.get("size", Types.Vector2D(20, 20)).x / 2
            r2 = other.data.get("size", Types.Vector2D(20, 20)).x / 2
            dx = self.position.x - other.position.x
            dy = self.position.y - other.position.y
            return dx * dx + dy * dy <= (r1 + r2) ** 2

        # --- Rettangolo vs Cerchio ---
        elif self.shape_type == Types.ShapeType.RECTANGLE and other.shape_type == Types.ShapeType.ELLIPSE:
            return self._rect_circle_collision(self, other)

        elif self.shape_type == Types.ShapeType.ELLIPSE and other.shape_type == Types.ShapeType.RECTANGLE:
            return self._rect_circle_collision(other, self)

        return False
    """

    def colliding(self, other: 'Actor'):
        size1 = self.data.get("size", Types.Vector2D(1, 1))
        size2 = other.data.get("size", Types.Vector2D(1, 1))
        align1 = self.data.get("align", Types.Align.CORNER)
        align2 = other.data.get("align", Types.Align.CORNER)

        rect1 = pygame.Rect(
            self.position.x -
            (0 if align1 == Types.Align.CORNER else size1.x / 2),
            self.position.y -
            (0 if align1 == Types.Align.CORNER else size1.y / 2),
            size1.x, size1.y
        )
        rect2 = pygame.Rect(
            other.position.x -
            (0 if align2 == Types.Align.CORNER else size2.x / 2),
            other.position.y -
            (0 if align2 == Types.Align.CORNER else size2.y / 2),
            size2.x, size2.y
        )

        return rect1.colliderect(rect2)

    def _rect_circle_collision(self, rect_actor, circle_actor):
        size = rect_actor.data.get("size", Types.Vector2D(1, 1))
        align = rect_actor.data.get("align", Types.Align.CORNER)
        radius = circle_actor.data.get("size", Types.Vector2D(20, 20)).x / 2

        rect_x = rect_actor.position.x - \
            (0 if align == Types.Align.CORNER else size.x / 2)
        rect_y = rect_actor.position.y - \
            (0 if align == Types.Align.CORNER else size.y / 2)
        rect = pygame.Rect(rect_x, rect_y, size.x, size.y)

        cx, cy = circle_actor.position.x, circle_actor.position.y
        closest_x = max(rect.left, min(cx, rect.right))
        closest_y = max(rect.top, min(cy, rect.bottom))

        dx = cx - closest_x
        dy = cy - closest_y
        return dx * dx + dy * dy <= radius ** 2


class Canvas:
    def __init__(self, screen: pygame.Surface, assetFolder):
        self.screen = screen
        self.assetFolder = assetFolder

    def fill(self, color: Types.Color):
        self.screen.fill(color)

    def draw(self, actor: Actor):
        if actor.shape_type == Types.ShapeType.RECTANGLE:
            size = actor.data.get("size", Types.Vector2D(1, 1))
            align = actor.data.get("align", Types.Align.CORNER)
            X = actor.position.x - \
                (0 if align == Types.Align.CORNER else size.x / 2)
            Y = actor.position.y - \
                (0 if align == Types.Align.CORNER else size.y / 2)
            pygame.draw.rect(self.screen, actor.data.get("color", Types.Color(0, 0, 0)),
                             pygame.Rect(X, Y, size.x, size.y))

        elif actor.shape_type == Types.ShapeType.ELLIPSE:
            size = actor.data.get("size", Types.Vector2D(50, 50))
            align = actor.data.get("align", Types.Align.CORNER)
            X = actor.position.x - \
                (0 if align == Types.Align.CORNER else size.x / 2)
            Y = actor.position.y - \
                (0 if align == Types.Align.CORNER else size.y / 2)
            pygame.draw.ellipse(self.screen, actor.data.get("color", Types.Color(0, 0, 0)),
                                pygame.Rect(X, Y, size.x, size.y))

        elif actor.shape_type == Types.ShapeType.SPRITE:
            size = actor.data.get("size", Types.Vector2D(1, 1))
            align = actor.data.get("align", Types.Align.CORNER)
            path = actor.data.get("path")
            alpha = actor.data.get("alpha", True)
            
            X = actor.position.x - \
                (0 if align == Types.Align.CORNER else size.x / 2)
            Y = actor.position.y - \
                (0 if align == Types.Align.CORNER else size.y / 2)
            
            if not path:
                raise KeyError("[ERROR] 'path' is required.")
            
            full_path = os.path.abspath(os.path.join(self.assetFolder, path))
            if not os.path.isfile(full_path):
                raise FileNotFoundError(f"[ERROR] File not found: {full_path}")

            image = pygame.image.load(full_path)
            image = image.convert_alpha() if alpha else image.convert()
            
            image = pygame.transform.smoothscale(image, size)
            
            self.screen.blit(image, (X,Y))
            
        elif actor.shape_type == Types.ShapeType.LINE:
            point1 = actor.position.x
            point2 = actor.position.y
            width = actor.data.get("width", 1)
            color = actor.data.get("color", Types.Color(0, 0, 0))
            pygame.draw.line(self.screen, color, point1, point2, width)

        elif actor.shape_type == Types.ShapeType.ARC:
            X = actor.position.x
            Y = actor.position.y
            size = actor.data.get("size", Types.Vector2D(1, 1))
            width = actor.data.get("width", 1)
            color = actor.data.get("color", Types.Color(0, 0, 0))
            start_angle = actor.data.get("start_angle", 3)
            stop_angle = actor.data.get("stop_angle", 0)
            pygame.draw.arc(self.screen, color, (X, Y, size.x,
                            size.y), start_angle, stop_angle, width)

        elif actor.shape_type == Types.ShapeType.TEXT:
            X = actor.position.x
            Y = actor.position.y
            text = actor.data.get("text", "")
            font = actor.data.get("font", Types.Font("Comic Sans MS", 20))
            color = actor.data.get("color", Types.Color(0, 0, 0))
            text_align = actor.data.get("text_align", Types.TextAlign.LEFT)
            antialias = actor.data.get("antialias", True)
            text_surface = font._construct().render(text, antialias, color)
            width, height = text_surface.get_width(), text_surface.get_height()
            
            if text_align == Types.TextAlign.CENTER:
                X -= width / 2
                Y -= height / 2
            elif text_align == Types.TextAlign.RIGHT:
                X -= width

            self.screen.blit(text_surface, (X, Y, width, height))


class Window:
    def __init__(self, FPS, assetFolder):
        self.display = pygame.display
        self._console_handle = ctypes.windll.kernel32.GetConsoleWindow()
        self.assetFolder = assetFolder
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
        
    def set_icon(self, iconAsset):          
        full_path = os.path.abspath(os.path.join(self.assetFolder, iconAsset))
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"[ERROR] File not found: {full_path}")
        
        image = pygame.image.load(full_path).convert_alpha()
        self.display.set_icon(image)

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
    def __init__(self, entry, assets):
        self.entry = entry
        self.assets = assets

    def log(self, text):
        print(f"[{time.strftime('%H:%M:%S')}] {text}")
        
    def get_entry_file(self):
        return self.entry
    
    def get_assets_folder(self):
        return self.assets
    
