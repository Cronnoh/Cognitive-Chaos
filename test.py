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

class FollowMouseSprite(Sprite):

    def __init__(self, image):
        super(FollowMouseSprite, self).__init__(image)
        self.position = (windowWidth/2, windowHeight/2)
        self.do(Repeat(Rotate(360,2)))
        window.push_handlers(self)

    def on_mouse_motion (self, x, y, dx, dy):
        posx, posy = director.get_virtual_coordinates(x,y)
        # self.position = (posx, posy)
        self.do(MoveTo((posx, posy), 0))
        # print(posx, posy)
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_mouse_motion(x, y, dx, dy)
        
    def on_mouse_press(self, x, y, buttons, modifiers):
        self.image = square2
        self.do(Repeat(Rotate(360,2)))
        
    def on_mouse_release(self, x, y, buttons, modifiers):
        self.image = square
        self.do(Repeat(Rotate(360,4)))

class MoveWall(Action):

    def __init__(self):
        super(MoveWall, self).__init__()
        
    def start(self):
        self.target.position = (windowWidth-self.target.width, self.target.initialY)
        self.target.do(MoveTo((-self.target.width,self.target.initialY),4))
    
    def step(self, dt):
        if self.target.x <= -self.target.width:
            self.target.wall.changeColor()
            self.start()

class Wall:
    images = [wall_gray, wall_blue, wall_green]
    def __init__(self):
        color = random.randrange(3)
        self.top = WallSprite(self.images[color], windowHeight, self)
        self.bottom = WallSprite(self.images[color], self.images[color].height, self)
        
    def addTo(self, layer):
        layer.add(self.top)
        layer.add(self.bottom)
        
    def changeColor(self):
        topColor = random.randrange(3)
        bottomColor = random.randrange(3)
        self.top.image = self.images[topColor]
        self.bottom.image = self.images[bottomColor]

class WallSprite(Sprite):
    def __init__(self, image, initialY, wall):
        super(WallSprite, self).__init__(image)
        self.wall = wall
        self.initialY = initialY
        self.image_anchor = (0, self.height)
        self.do(MoveWall())

window = director.init(
   windowWidth,
   windowHeight,
   caption="test")
   
layer = Layer()
sprite = FollowMouseSprite(square)
wall = Wall()
layer.add(sprite)
wall.addTo(layer)

scene = scene.Scene(layer)
director.run(scene)
