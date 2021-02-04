from cocos import *
from cocos.layer import *
from cocos.director import *
from cocos.actions import *
from cocos.sprite import *

import Wall
from Resources import *

class Cursor(Sprite):
    def __init__(self, image):
        super(Cursor, self).__init__(image)
        self.position = (windowWidth/2, gameAreaHeight/2)
        self.do(Repeat(Rotate(360,2)))
        self.colr = 1
        self.radius = self.width/2
        window.push_handlers(self)

    def on_mouse_motion (self, x, y, dx, dy):
        x,y = director.get_virtual_coordinates(x,y)
        x = min(x, windowWidth)
        x = max(x, 0)
        y = min(y, gameAreaHeight)
        y = max(y, 0)
        self.position = x,y
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_mouse_motion(x, y, dx, dy)
        
    def speedUp(self):
        self.image = cursor_green
        self.colr = 2
        self.do(Repeat(Rotate(360,2)))
        
    def slowDown(self):
        self.image = cursor_blue
        self.colr = 1
        self.do(Repeat(Rotate(360,4)))

    def reverse(self):
        self.image = cursor_blue
        self.colr = 3
        self.do(Repeat(Rotate(-360,2)))

class GameLayer(Layer):
    levels = [level1, level2, level3, level4, level5]
    def __init__(self):
        super(GameLayer, self).__init__()
        self.add(Sprite(top, position=(windowWidth/2, windowHeight-20)), z=2)
        self.levelSprite = Sprite(level1, position=(windowWidth/2, windowHeight/2))
        self.add(self.levelSprite, z=1)
        self.add(Sprite(bg, position=(windowWidth/2, windowHeight/2)), z=-1)
        self.level = 0
        self.slow = 500
        self.fast = 1000
        self.cursor = Cursor(cursor_blue)
        self.walls = [Wall.Wall(4, self.slow)]
        self.walls[0].addTo(self)
        self.add(self.cursor)
        self.do(Repeat(CallFunc(self.update)))
        # Delay
        window.push_handlers(self)

    def update(self):
        for wall in self.walls:
            wall.checkCollision(self.cursor)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons == pyglet.window.mouse.RIGHT:
            self.rightMouse()
            return
        self.cursor.speedUp()
        self.level = (self.level+1) % 5
        self.levelSprite.image = self.levels[self.level]
        for wall in self.walls:
            wall.changeSpeed(self.fast)
        
    def rightMouse(self):
        self.cursor.reverse()
        for wall in self.walls:
            wall.changeSpeed(-self.fast)

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.cursor.slowDown()
        for wall in self.walls:
            wall.changeSpeed(self.slow)


window = director.init(
   windowWidth,
   windowHeight,
   caption="test")
   
layer = GameLayer()
scene = scene.Scene(layer)
director.run(scene)
