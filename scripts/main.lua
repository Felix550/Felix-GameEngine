function On_Start()
    --Window.hide_console()
    Window.set_icon("sprite1.png")
    Window.set_title("Running...")
    Window.set_size(Vector2D(800, 600))
    Window.set_target_fps(60)

    Debug.log(Debug.get_entry_file())
    Debug.log(Debug.get_assets_folder())
end

local cube = Actor(
    Vector2D(35, 35),
    ShapeType.RECTANGLE,
    {
        color = Color(255, 0, 0),
        size = Vector2D(50, 50),
        align = Align.CENTER
    }
)

local ellipse = Actor(
    Vector2D(110, 35),
    ShapeType.ELLIPSE,
    {
        color = Color(0, 0, 255),
        size = Vector2D(50, 50),
        align = Align.CENTER
    }
)

local line = Actor(
    Vector2D(
        Vector2D(10, 75),
        Vector2D(135, 75)),
    ShapeType.LINE,
    {
        color = Color(0, 0, 0),
        width = 5
    }
)

local arc = Actor(
    Vector2D(10, 35),
    ShapeType.ARC,
    {
        size = Vector2D(125, 125),
        color = Color(0, 0, 0),
        start_angle = 3.14,
        stop_angle = 0,
        width = 1
    }
)

local font = Font("Arial",30,true,true)

local text = Actor(
    Vector2D(800, 0),
    ShapeType.TEXT,
    {
        font = font,
        color = Color(0, 0, 0),
        antialias = true,
        text_align = TextAlign.RIGHT
    }
)

local image = Actor(
    Vector2D(400, 300),
    ShapeType.SPRITE,
    {
        size = Vector2D(100,100),
        path = "sprite1.png",
        alpha = true,
        align = Align.CENTER
    }
)

local currentPlayerTEXT = Actor(
    Vector2D(Window.get_size().x / 2, Window.get_size().y - 20),
    ShapeType.TEXT,
    {
        text = "1  2  3",
        font = font,
        color = Color(0, 0, 0),
        antialias = true,
        text_align = TextAlign.CENTER
    }
)

local currentPlayerSELECTOR = Actor(
    Vector2D(Window.get_size().x / 2 - 32, Window.get_size().y - 20),
    ShapeType.RECTANGLE,
    {
        size = Vector2D(18,32),
        color = Color(255, 0, 0),
        align = TextAlign.CENTER
    }
)

-- Velocità movimento
local speed = 300

-- Player attivo
local player = cube

local function moveControl(dt)
    -- Cambia il player attivo
    if Input.GetKeyUp(KeyCode.K_1) then
        player = cube
    elseif Input.GetKeyUp(KeyCode.K_2) then
        player = ellipse
    elseif Input.GetKeyUp(KeyCode.K_3) then
        player = image
    end

    -- Movimento del player attivo
    local pos = player.get_pos()
    local size = player.get_data("size")
    local winSize = Window.get_size()

    if Input.GetKey(KeyCode.K_RIGHT) then
        pos = Vector2D(pos.x + speed * dt, pos.y)
    end
    if Input.GetKey(KeyCode.K_LEFT) then
        pos = Vector2D(pos.x - speed * dt, pos.y)
    end
    if Input.GetKey(KeyCode.K_UP) then
        pos = Vector2D(pos.x, pos.y - speed * dt)
    end
    if Input.GetKey(KeyCode.K_DOWN) then
        pos = Vector2D(pos.x, pos.y + speed * dt)
    end

    -- Clamping nei bordi finestra
    pos = Vector2D(
        math.max(size.x / 2, math.min(pos.x, winSize.x - size.x / 2)),
        math.max(size.y / 2, math.min(pos.y, winSize.y - size.y / 2))
    )

    player.set_pos(pos)
end

function On_Runtime(dt, fps, frame)
    Canvas.fill(Color(255, 255, 255))

    Window.set_title("FPS: " .. tostring(fps))
    text.change_data("text","FPS: " .. string.format("%.0f", fps))

    moveControl(dt)

    if cube.colliding(ellipse) then
        Debug.log("COLLIDE Ellipse & Cube")
    end

    if player == cube then
        currentPlayerSELECTOR.set_pos(Vector2D(Window.get_size().x / 2 - 32,Window.get_size().y - 20))
    elseif player == ellipse then
        currentPlayerSELECTOR.set_pos(Vector2D(Window.get_size().x / 2,Window.get_size().y - 20))
    elseif player == image then
        currentPlayerSELECTOR.set_pos(Vector2D(Window.get_size().x / 2 + 32,Window.get_size().y - 20))
    end

    local tsize = text.get_size()
    Debug.log(tsize.x .. " : " .. tsize.y)

    -- Disegna gli attori
    Canvas.draw(cube)
    Canvas.draw(ellipse)
    Canvas.draw(line)
    Canvas.draw(arc)
    Canvas.draw(text)
    Canvas.draw(image)
    --Logic
    Canvas.draw(currentPlayerSELECTOR)
    Canvas.draw(currentPlayerTEXT)
end
