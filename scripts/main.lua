function On_Start()
    --Window.hide_console()
    Window.set_title("Running...")
    Window.set_size(Vector2D(800,600))
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

local sprite = Actor(
    Vector2D(25, 25),
    ShapeType.SPRITE,
    {size = Vector2D(50, 50)}
)

-- Velocità movimento
local speed = 300

-- Player attivo
local player = cube

function On_Runtime(dt, fps, frame)
    Canvas.fill(Color(255, 255, 255))

    Window.set_title("FPS: " .. tostring(fps))

    -- Cambia il player attivo
    if Input.GetKeyUp(KeyCode.K_1) then
        player = cube
    elseif Input.GetKeyUp(KeyCode.K_2) then
        player = sprite
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

    -- Disegna gli attori
    Canvas.draw(cube)
    Canvas.draw(sprite)

    -- Bordo nero per evidenziare il player attivo
    local borderPos = player.get_pos()
    local borderSize = player.get_data("size")
    local topLeft = Vector2D(borderPos.x - borderSize.x / 2, borderPos.y - borderSize.y / 2)

    -- Disegna un rettangolo nero come contorno
    Canvas.draw_rect_outline(topLeft, borderSize, Color(0, 0, 0), 3)
end
