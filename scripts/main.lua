function On_Start()
    --Window.hide_console()
    Window.set_title("Running...")
    Window.set_size(Vector2D(800, 600))
    Window.set_target_fps(60)
end

local cube = Actor(
    Vector2D(25, 25),
    ShapeType.RECTANGLE,
    {
        color = Color(255, 0, 0),
        size = Vector2D(50, 50),
        align = Align.CENTER
    }
)

local ellipse = Actor(
    Vector2D(50, 50),
    ShapeType.ELLIPSE,
    {
        color = Color(0, 0, 255),
        size = Vector2D(50, 50),
        align = Align.CENTER
    }
)

local line = Actor(
    Vector2D(
        Vector2D(0, 0),
        Vector2D(100, 100)),
    ShapeType.LINE,
    {
        color = Color(0, 0, 0),
        width = 5
    }
)

local arc = Actor(
    Vector2D(150, 150),
    ShapeType.ARC,
    {
        size = Vector2D(50, 50),
        color = Color(0, 0, 0),
        start_angle = 0,
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

    moveControl(dt)

    if cube.colliding(ellipse) then
        -- Debug.log("UIUUAUAUA")
    end

    text.change_data("text",string.format("%.0f", fps))

    -- Disegna gli attori
    Canvas.draw(cube)
    Canvas.draw(ellipse)
    Canvas.draw(line)
    Canvas.draw(arc)
    Canvas.draw(text)
end
