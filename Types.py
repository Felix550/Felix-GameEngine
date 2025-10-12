from enum import Enum
from types import SimpleNamespace
import pygame

class ShapeType(Enum):
    RECTANGLE = 1
    CIRCLE = 2
    SPRITE = 3
    
class Align(Enum):
    CENTER = 1
    CORNER = 2

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