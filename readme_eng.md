# Felix Game Engine - User Lua API

## • Types

### `Color(r, g, b, a=1)`
Represents an RGBA color.
- **r**: red component (0–255)
- **g**: green component (0–255)
- **b**: blue component (0–255)
- **a**: alpha (0–1)

### `Vector2D(x, y)`
Represents a 2D vector.
- **x**: X coordinate
- **y**: Y coordinate

#### Functions:
- `Vector2D.add(Vector2D || int || float)` → adds a value to the Vector2D
- `Vector2D.sub(Vector2D || int || float)` → subtracts a value from the Vector2D

### `ShapeType`
Defines the shape of an actor.
- `RECTANGLE`: rectangle
- `ELLIPSE`: circle / ellipse
- `SPRITE`: sprite (not yet implemented)
- `LINE`: line
- `ARC`: arc
- `TEXT`: text

### `Align`
Defines drawing alignment.
- `CENTER`: centers the shape at the specified point
- `CORNER`: draws from the top-left corner

### `TextAlign`
Defines text alignment.
- `LEFT`: aligns text to top-left
- `CENTER`: aligns text to center
- `RIGHT`: aligns text to top-right

### `KeyCode`
Defines keyboard key codes.
- `K_`: all key codes start with K_

### `MouseButton`
Defines mouse buttons.
- `LEFT`: left button
- `MIDDLE`: middle button
- `RIGHT`: right button

---

## • Objects

### `Actor(position, shape_type, data)`
Creates a drawable object.
- **position**: `Vector2D` actor position
- **shape_type**: shape type (`ShapeType`)
- **data**: property dictionary (see `Shape Data`)

#### Functions:
- `Actor.move(deltaPosition)` → moves the actor
- `Actor.set_pos(newPosition)` → sets absolute position
- `Actor.get_pos()` → gets absolute position
- `Actor.change_data(key, value)` → modifies a property in `data`
- `Actor.get_data(key)` → retrieves a property from `data`
- `Actor.get_size()` → gets rendered text size (used only if ShapeType is TEXT)
- `Actor.colliding(Actor)` → returns True if two `Actor`s collide

---

### `Font(fontName, fontSize, bold (false), italic (false))`
Creates a font object.
- **fontName**: system font name
- **fontSize**: font size
- **bold**: True for bold text
- **italic**: True for italic text

---

### `Canvas`
Represents the drawing surface.

#### Functions:
- `Canvas.fill(color)` → fills the screen with a color
- `Canvas.draw(actor)` → draws an `Actor`

---

### `Window`
Manages window properties.

#### Functions:
- `Window.set_title(title)` → sets window title
- `Window.get_title()` → returns current title
- `Window.set_size(Vector2D)` → sets window size
- `Window.get_size()` → returns size (`Vector2D`)
- `Window.set_target_fps(fps)` → sets target framerate
- `Window.get_target_fps()` → returns current framerate
- `Window.toggle_fullscreen()` → toggles fullscreen/windowed
- `Window.show_console()` → shows console
- `Window.hide_console()` → hides console
- `Window.set_icon(path)` → sets window icon (relative to assets folder)

### `Screen`
Manages screen properties.

#### Functions:
- `Screen.get_size()` → returns the physical screen resolution

---

### `Mouse`
Manages mouse input.

#### Functions:
- `Mouse.get_pos()` → returns position (`Vector2D`)
- `Mouse.set_pos(Vector2D)` → sets cursor position
- `Mouse.GetButton(MouseButton)` → returns True if button is held
- `Mouse.GetButtonDown(MouseButton)` → True if button was pressed this frame
- `Mouse.GetButtonUp(MouseButton)` → True if button was released this frame

### `Input`
Manages keyboard input.

#### Functions:
- `Input.GetKey(KeyCode)` → True if key is held
- `Input.GetKeyDown(KeyCode)` → True if key was pressed this frame
- `Input.GetKeyUp(KeyCode)` → True if key was released this frame

---

### `Debug`
Basic logging system.

#### Functions:
- `Debug.log(text)` → prints a message with timestamp
- `Debug.get_entry_file()` → returns the absolute path of the main .lua file
- `Debug.get_assets_folder()` → returns the absolute path of the assets folder

---

## • Shape Data

### `RECTANGLE`
A rectangle (or square).

#### Data properties:
- **size**: `Vector2D` rectangle size
- **color**: `Color` rectangle color
- **align**: `Align` pivot alignment

---

### `ELLIPSE`
An ellipse (or circle).

#### Data properties:
- **size**: `Vector2D` ellipse size
- **color**: `Color` ellipse color
- **align**: `Align` pivot alignment

---

### `SPRITE`
An image.

#### Data properties:
- **path**: relative path to the asset
- **size**: `Vector2D` image size
- **align**: `Align` pivot alignment
- **alpha**: if True, uses alpha transparency

---

### `LINE`
A line.

#### Data properties:
- Positional parameter is a series of 2 points:  
  `Vector2D(Vector2D(x1,y1), Vector2D(x2,y2))`
- **color**: `Color` line color
- **width**: line thickness

### `ARC`
An arc.

#### Data properties:
- **size**: `Vector2D` arc size
- **color**: `Color` arc color
- **start_angle**: start angle
- **stop_angle**: end angle
- **width**: line thickness

---

### `TEXT`
A text object.

#### Data properties:
- **text**: text content
- **color**: `Color` text color
- **font**: `Font` font object
- **text_align**: `TextAlign` alignment
- **antialias**: True to enable antialiasing

---

## • Global functions

### `wait(seconds: float)`
Pauses execution (engine thread) for the given number of seconds.

---

## • Main Lua functions

### `On_Start()`
Called once when the script starts.

### `On_Runtime(deltaTime: float, fps: float, frame: int)`
Called every frame.
- **deltaTime**: time since last frame (seconds)
- **fps**: current framerate
- **frame**: current frame index

### `On_KeyDown(key: KeyCode)`
Called when a key is pressed.
- **key**: pressed key

### `On_KeyUp(key: KeyCode)`
Called when a key is released.
- **key**: released key
