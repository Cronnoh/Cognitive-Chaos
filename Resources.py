import pyglet

windowWidth = 1280
windowHeight = 720
hudHeight = 40
gameAreaHeight = windowHeight-hudHeight

cursor_blue = pyglet.resource.image('images/cursor_blue.png')
cursor_green = pyglet.resource.image('images/cursor_green.png')

wall_gray = pyglet.resource.image('images/wall_gray.png')
wall_green = pyglet.resource.image('images/wall_green.png')
wall_blue = pyglet.resource.image('images/wall_blue.png')

top = pyglet.resource.image('images/top.png')
bg = pyglet.resource.image('images/bg.png')

levels = [
    pyglet.resource.image('images/level1.png'),
    pyglet.resource.image('images/level2.png'),
    pyglet.resource.image('images/level3.png'),
    pyglet.resource.image('images/level4.png'),
    pyglet.resource.image('images/level5.png')
]