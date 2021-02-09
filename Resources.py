# Connor Hesseling
# CPS 499
# Project 1

import pyglet

windowWidth = 1280
windowHeight = 720
hudHeight = 40
gameAreaHeight = windowHeight-hudHeight


cursor_blue = pyglet.resource.image('images/cursor_blue.png')
cursor_green = pyglet.resource.image('images/cursor_green.png')
cursor_red = pyglet.resource.image('images/cursor_red.png')

wallImages = [
    pyglet.resource.image('images/wall_gray.png'),
    pyglet.resource.image('images/wall_blue.png'),
    pyglet.resource.image('images/wall_green.png'),
    pyglet.resource.image('images/wall_red.png')
]

top = pyglet.resource.image('images/top.png')
bg = pyglet.resource.image('images/bg.png')
tutorial = pyglet.resource.image('images/tutorial.png')

levels = [
    pyglet.resource.image('images/level1.png'),
    pyglet.resource.image('images/level2.png'),
    pyglet.resource.image('images/level3.png'),
    pyglet.resource.image('images/level4.png'),
    pyglet.resource.image('images/level5.png')
]