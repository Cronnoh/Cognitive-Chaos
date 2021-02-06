from cocos import *
from cocos.actions import *
from cocos.sprite import *
import random

from Resources import *

class Wall:

    def __init__(self, pieceNum, initialSpeed, position):
        initialX = windowWidth - position*384
        self.pieces = [WallSprite(wallImages[0], initialX, gameAreaHeight, initialSpeed, self, top=True)]
        for i in range(1,pieceNum):
            height = gameAreaHeight - wallImages[0].height*i
            self.pieces.append(WallSprite(wallImages[0], initialX, height, initialSpeed, self))
        self.changeColor()
        self.collide = False
        self.canActivate = False

    def activate(self):
        self.collide = True
        self.canActivate = False
        for piece in self.pieces:
            piece.opacity = 255
        
    def addTo(self, layer):
        for piece in self.pieces:
            layer.add(piece)
        
    def changeColor(self):
        total = 0
        for piece in self.pieces:
            piece.colr = random.randrange(len(wallImages))
            piece.image = wallImages[piece.colr]
            total += piece.colr
        
        # if all the pieces are gray, pick one and make it not gray
        if total == 0:
            piece = self.pieces[random.randrange(len(self.pieces))]
            piece.colr = random.randrange(1,len(wallImages))
            piece.image = wallImages[piece.colr]

    def allGray(self):
        for piece in self.pieces:
            piece.colr = 0
            piece.image = wallImages[piece.colr]

    def changeSpeed(self, speed):
        for piece in self.pieces:
            piece.speed = speed

    def checkCollision(self, cursor):
        if not self.collide:
            return
        for piece in self.pieces:
            intersectH = (cursor.x+cursor.radius) > piece.x and (cursor.x-cursor.radius) < (piece.x+piece.width)
            intersectV = (cursor.y-cursor.radius) < piece.y and (cursor.y+cursor.radius) > (piece.y-piece.height)
            if intersectH and intersectV:
                print("collision: " + str(cursor.colr) + " " + str(piece.colr))
                if cursor.colr != piece.colr:
                    print("Lose")

class WallSprite(Sprite):
    def __init__(self, image, initialX, initialY, initialSpeed, wall, top=False):
        super(WallSprite, self).__init__(image)
        self.wall = wall
        self.initialX = initialX
        self.initialY = initialY
        self.speed = initialSpeed
        self.colr = 0
        self.image_anchor = (0, self.height)
        self.top = top
        self.do(MoveWall())
        self.opacity = 0

class MoveWall(Action):

    def __init__(self):
        super(MoveWall, self).__init__()
        
    def start(self):
        print(self.target.initialX)
        self.target.position = (self.target.initialX, self.target.initialY)
    
    def step(self, dt):
        self.target.x += -self.target.speed * dt
        if self.target.x < -self.target.width-128:
            if self.target.wall.canActivate:
                self.target.wall.activate()
            if self.target.top == True:
                self.target.wall.changeColor()
            self.target.position = (windowWidth, self.target.initialY)
        elif self.target.x > windowWidth+128:
            if self.target.top == True:
                self.target.wall.allGray()
            self.target.position = (-self.target.width, self.target.initialY)
