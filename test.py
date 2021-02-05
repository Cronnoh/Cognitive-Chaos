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
    def __init__(self):
        super(GameLayer, self).__init__()
        self.slow = 500
        self.fast = 1000
        self.cursor = Cursor(cursor_blue)
        self.walls = [Wall.Wall(4, self.slow)]
        self.walls[0].addTo(self)
        self.add(self.cursor)
        self.score = Score(self.cursor)
        self.score.do(Repeat(Delay(.1) + CallFunc(self.score.update)))
        # Delay
        window.push_handlers(self)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons == pyglet.window.mouse.RIGHT:
            self.rightMouse()
            return
        self.score.modifier = 2
        self.cursor.speedUp()
        for wall in self.walls:
            wall.changeSpeed(self.fast)
        
    def rightMouse(self):
        self.cursor.reverse()
        self.score.modifier = -5
        for wall in self.walls:
            wall.changeSpeed(-self.fast)

    def on_mouse_release(self, x, y, buttons, modifiers):
        self.cursor.slowDown()
        self.score.modifier = 1
        for wall in self.walls:
            wall.changeSpeed(self.slow)

class Score(text.Label):
    def __init__(self, cursor):
        super(Score, self).__init__("0")
        self.font_name="sans-serif",
        self.font_size=32
        self.position = (25, windowHeight-25)
        self.modifier = 1
        self.value = 0
        self.cursor = cursor
        self.level = 1
        
    def update(self):
        if self.cursor.x >= windowWidth/2 and self.modifier > 0:
            bonus = 2
        else:
            bonus = 1
        print(self.modifier * self.level * bonus)
        self.value += self.modifier * self.level * bonus
        self.element.text = str(self.value)

class MainScene(scene.Scene):
    def __init__(self):
        super(MainScene, self).__init__()
        self.gameLayer = GameLayer()
        self.add(self.gameLayer)
        levelSprite = Sprite(levels[0], position=(windowWidth/2, windowHeight/2))
        self.add(Sprite(top, position=(windowWidth/2, windowHeight-20)), z=2)
        self.add(levelSprite, z=1)
        self.add(Sprite(bg, position=(windowWidth/2, windowHeight/2)), z=-1)
        self.add(self.gameLayer.score, z=3)
        self.level = 0

        self.do(Repeat(CallFunc(self.update)))

    def update(self):
        for wall in self.gameLayer.walls:
            wall.checkCollision(self.gameLayer.cursor)

    def increaseLevel():
        self.gameLayer.increaseLevel()
        self.levelSprite = level[self.level]

window = director.init(
   windowWidth,
   windowHeight,
   caption="test")

main = MainScene()
director.run(main)
