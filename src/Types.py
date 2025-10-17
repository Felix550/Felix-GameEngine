from enum import Enum
from types import SimpleNamespace
import pygame
import math

class ShapeType(Enum):
    RECTANGLE = 1
    ELLIPSE = 2
    SPRITE = 3
    LINE = 4
    ARC = 5
    TEXT = 6
    
class Align(Enum):
    CENTER = 1
    CORNER = 2
    
class TextAlign(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3
    
class Font():
    def __init__(self,fontName,fontSize, bold: bool = False, italic: bool = False):
        self.fontName = fontName
        self.fontSize = fontSize
        self.bold = bold
        self.italic = italic
    
    def _construct(self):
        return pygame.font.SysFont(self.fontName,self.fontSize,self.bold, self.italic)
    
        
#Inputs
KeyCode = SimpleNamespace(**{name: value for name, value in pygame.__dict__.items() if name.startswith("K_")})

class MouseButton():
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

class Color:
    def __init__(self, r, g, b, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a * 255

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b
        yield self.a

    def __len__(self):
        return 4

    def __getitem__(self, key):
        if isinstance(key, int):
            return [self.r, self.g, self.b, self.a][key]
        elif isinstance(key, str) and hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"{key} not found")


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if isinstance(key, int):
            return [self.x, self.y][key]
        elif isinstance(key, str) and hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"{key} not found")

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Vector2D(self.x + other, self.y + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Vector2D(self.x - other, self.y - other)
        return NotImplemented
    
    def __mul__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):
            return Vector2D(self.x * other, self.y * other)
        return NotImplemented
    
    def __truediv__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)
        elif isinstance(other, (int, float)):
            return Vector2D(self.x / other, self.y / other)
        return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Vector2D):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, (int, float)):
            self.x += other
            self.y += other
        else:
            raise TypeError("Unsupported type for in-place addition")
        return self

    def __isub__(self, other):
        if isinstance(other, Vector2D):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, (int, float)):
            self.x -= other
            self.y -= other
        else:
            raise TypeError("Unsupported type for in-place subtraction")
        return self
    
    #LUA
    def add(self, other):
        if isinstance(other, Vector2D):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, (int,float)):
            self.x += other
            self.y += other
            
    def sub(self, other):
        if isinstance(other, Vector2D):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, (int,float)):
            self.x -= other
            self.y -= other
            
    def rotate(self, angle_degrees):
        """Ruota il vettore di un angolo in gradi"""
        angle_rad = math.radians(angle_degrees)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        
        new_x = self.x * cos_angle - self.y * sin_angle
        new_y = self.x * sin_angle + self.y * cos_angle
        
        return Vector2D(new_x, new_y)
    
    def get_angle(self):
        """Restituisce l'angolo del vettore in gradi"""
        return math.degrees(math.atan2(self.y, self.x))
    
    def set_angle(self, angle_degrees):
        """Imposta l'angolo del vettore mantenendo la lunghezza"""
        length = self.get_length()
        angle_rad = math.radians(angle_degrees)
        self.x = length * math.cos(angle_rad)
        self.y = length * math.sin(angle_rad)
    
    def get_length(self):
        """Restituisce la lunghezza del vettore"""
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def set_length(self, length):
        """Imposta la lunghezza del vettore mantenendo l'angolo"""
        angle = math.atan2(self.y, self.x)
        self.x = length * math.cos(angle)
        self.y = length * math.sin(angle)