class excecuter:
    def __init__(self, assetFolder, entryFile):
        self.assetFolder = assetFolder
        self.entryFile = entryFile
    
    def run(self,luaCode):
        import pygame
        from lupa import LuaRuntime
        import time
        import Types
        import Objects

        lua = LuaRuntime(unpack_returned_tuples=True)

        pygame.init()
        pygame.font.init()

        Screen = Objects.Screen()
        lua.globals().Screen = Screen

        screen = pygame.display.set_mode((800,600))
        clock = pygame.time.Clock()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)

        #Typess
        lua.globals().Color = Types.Color
        lua.globals().Vector2D = Types.Vector2D
        lua.globals().ShapeType = Types.ShapeType
        lua.globals().Align = Types.Align
        lua.globals().TextAlign = Types.TextAlign
        lua.globals().Font = Types.Font
        
        #KeyCode
        lua.globals().KeyCode = Types.KeyCode
        lua.globals().MouseButton = Types.MouseButton

        #Objects
        Canvas = Objects.Canvas(screen,self.assetFolder)
        lua.globals().Canvas = Canvas
        Debug = Objects.Debug(self.entryFile, self.assetFolder)
        lua.globals().Debug = Debug
        Window = Objects.Window(60, self.assetFolder)
        lua.globals().Window = Window
        # -- Screen --
        Mouse = Objects.Mouse()
        lua.globals().Mouse = Mouse
        Input = Objects.Input()
        lua.globals().Input = Input

        #Unizilized Objects
        lua.globals().Actor = Objects.Actor

        #Functions
        lua.globals().wait = time.sleep
        
        lua.execute(luaCode)
            
        On_Runtime = lua.globals().On_Runtime if "On_Runtime" in lua.globals() else None
        On_Start = lua.globals().On_Start if "On_Start" in lua.globals() else None
        On_KeyDown = lua.globals().On_KeyDown if "On_KeyDown" in lua.globals() else None
        On_KeyUp = lua.globals().On_KeyUp if "On_KeyUp" in lua.globals() else None

        startTime = time.perf_counter()
        currentFrame = 0

        if On_Start is not None:
            On_Start()

        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN:
                    if On_KeyDown is not None:
                        On_KeyDown(e.key)
                elif e.type == pygame.KEYUP:
                    if On_KeyUp is not None:
                        On_KeyUp(e.key)         
            
            if currentFrame <= Window.get_target_fps():
                screen.fill((0,0,0))
                text_surface = my_font.render('Made With Felix Engine', True, (255, 255, 255))
                w,h = screen.get_size()
                screen.blit(text_surface, ((w - text_surface.get_width()) / 2,(h - text_surface.get_height()) / 2))
                pygame.display.flip()
                clock.tick(Window.get_target_fps())
                currentFrame += 1
                continue
            
            Input._update()
            Mouse._update()
            
            deltaTime = time.perf_counter()      
            if On_Runtime is not None:
                On_Runtime(deltaTime - startTime,clock.get_fps(),currentFrame)
            
            startTime = deltaTime
            
            Input._end_frame()
            Mouse._end_frame()
            
            currentFrame += 1
                
            pygame.display.flip()
            clock.tick(Window.get_target_fps())