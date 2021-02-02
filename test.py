from cocos import *
from cocos.layer import *
from cocos.director import *
from cocos.actions import *
from cocos.sprite import *
import random

windowWidth = 1184
windowHeight = 666

square = pyglet.resource.image('square.png')
square2 = pyglet.resource.image('square2.png')
wall_gray = pyglet.resource.image('wall.png')
wall_green = pyglet.resource.image('wall_green.png')
wall_blue = pyglet.resource.image('wall_blue.png')

class Cursor(Sprite):
    def __init__(self, image):
        super(Cursor, self).__init__(image)
        self.position = (windowWidth/2, windowHeight/2)
        self.do(Repeat(Rotate(360,2)))
        self.c = 1
        window.push_handlers(self)

    def on_mouse_motion (self, x, y, dx, dy):
        self.position = director.get_virtual_coordinates(x,y)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_mouse_motion(x, y, dx, dy)
        
    def speedUp(self):
        self.image = square2
        self.c = 2
        self.do(Repeat(Rotate(360,2)))
        
    def slowDown(self):
        self.image = square
        self.c = 1
        self.do(Repeat(Rotate(360,4)))

class MoveWall(Action):

    def __init__(self):
        super(MoveWall, self).__init__()
        
    def start(self):
        self.target.position = (windowWidth+self.target.width, self.target.initialY)
    
    def step(self, dt):
        self.target.x += -self.target.speed * dt
        if self.target.x <= -self.target.width:
            if self.target.top == True:
                self.target.wall.changeColor()
            self.start()

class Wall:
    images = [wall_gray, wall_blue, wall_green]

    def __init__(self, initialSpeed):
        self.pieces = [WallSprite(self.images[0], windowHeight, initialSpeed, self, top=True), WallSprite(self.images[0], self.images[0].height, initialSpeed, self)]
        self.changeColor()
        
    def addTo(self, layer):
        for piece in self.pieces:
            layer.add(piece)
        
    def changeColor(self):
        total = 0
        for piece in self.pieces:
            piece.c = random.randrange(3)
            piece.image = self.images[piece.c]
            total += piece.c
        
        # if all the pieces are gray, pick one and make it not gray
        if total == 0:
            piece = self.pieces[random.randrange(len(self.pieces))]
            piece.c = random.randrange(1,3)
            piece.image = self.images[piece.c]

    def changeSpeed(self, speed):
        for piece in self.pieces:
            piece.speed = speed

    def checkCollision(self, cursor):
        for piece in self.pieces:
            intersectH = cursor.x > piece.x and cursor.x < (piece.x+piece.width)
            intersectV = cursor.y < piece.y and cursor.y > (piece.y-piece.height)
            if intersectH and intersectV:
                print("collision: " + str(cursor.c) + " " + str(piece.c))
                if cursor.c != piece.c:
                    print("Lose")


class WallSprite(Sprite):
    def __init__(self, image, initialY, initialSpeed, wall, top=False):
        super(WallSprite, self).__init__(image)
        self.wall = wall
        self.initialY = initialY
        self.speed = initialSpeed
        self.c = 0
        self.image_anchor = (0, self.height)
        self.top = top
        self.do(MoveWall())

class GameLayer(Layer):
    def __init__(self):
        super(GameLayer, self).__init__()
        self.slow = 500
        self.fast = 1000
        self.cursor = Cursor(square)
        self.walls = [Wall(self.slow)]
        self.walls[0].addTo(self)
        self.add(self.cursor)
        self.do(Repeat(CallFunc(self.update)))
        # Delay
        window.push_handlers(self)

    def update(self):
        for wall in self.walls:
            wall.checkCollision(self.cursor)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.cursor.speedUp()
        for wall in self.walls:
            wall.changeSpeed(self.fast)
        
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
