function On_Start()
    Window.hide_console()
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

local speed = 1000

local player = cube

function On_Runtime(dt, fps, frame)
    Canvas.fill(Color(255, 255, 255))

    Window.set_title(dt .. " : " .. fps .. " : " .. frame)

    local cubePos = player.get_pos()
    local cubeSize = player.get_data("size")
    local windowSize = Window.get_size()

    local newX = cubePos.x
    local newY = cubePos.y

    if Input.GetKey(KeyCode.K_RIGHT) then
        newX = newX + speed * dt
    end
    if Input.GetKey(KeyCode.K_LEFT) then
        newX = newX - speed * dt
    end
    if Input.GetKey(KeyCode.K_UP) then
        newY = newY - speed * dt
    end
    if Input.GetKey(KeyCode.K_DOWN) then
        newY = newY + speed * dt
    end

    if Input.GetKeyUp(KeyCode.K_1) then
        player = cube
    elseif Input.GetKeyUp(KeyCode.K_2) then
        player = sprite
    end

    -- Clampa la posizione per rimanere nei bordi
    newX = math.max(cubeSize.x / 2, math.min(newX, windowSize.x - cubeSize.x / 2))
    newY = math.max(cubeSize.y / 2, math.min(newY, windowSize.y - cubeSize.y / 2))

    player.set_pos(Vector2D(newX, newY))

    Canvas.draw(cube)
    Canvas.draw(sprite)
end
