function On_Start()
   Window.set_title("NIGGER")
end

local cube = Actor(Vector2D(25, 25), ShapeType.RECTANGLE, { color = Color(255, 0, 0), width = 50, height = 50, align = Align.CENTER})

local dirX = 1
local dirY = 0


function On_Runtime(dt)
   Canvas.fill(Color(0,255,0))

   if cube.GetPos().x >= 800 - 25 and dirX == 1 then
      Debug.Log("NIGGA X")
      dirX = 0
      dirY = 1
   end
   cube.Move(Vector2D(150 * dt * dirX,150 * dt * dirY))

   Canvas.Draw(cube)
end