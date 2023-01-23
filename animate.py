#
# Experimentation with the animation module Pyglet

import pyglet
import math

# Create the background
window = pyglet.window.Window()
stockholm = pyglet.resource.image('res/map.stockholm.png')
print(window.width, window.height)


# Create the sprites
sprites = []

uav = pyglet.resource.image('res/uav1-wide-af-color.png')
uav.anchor_x = uav.width // 2
uav.anchor_y = uav.height // 2
sprites.append([pyglet.sprite.Sprite(uav, x=window.width/2, y=window.height/2), window.width/2, window.height/2])

cs = pyglet.resource.image('res/circle.png')

for mysprite in sprites:
    mysprite[0].scale = 0.15
    mysprite[0].velocity = (0, 0)

# Helpers
limit = lambda x, lower, upper: lower if x < lower else upper if x > upper else x


@window.event
def on_draw():
    window.clear()
    stockholm.blit(0, 0)
    for mysprite in sprites:
        mysprite[0].draw()
    return


@window.event
def on_mouse_press(x, y, button, modifiers):
    if (button == pyglet.window.mouse.LEFT):
        sprites[0][1] = x
        sprites[0][2] = y
    elif (button == pyglet.window.mouse.RIGHT):
        sprites[0][0].rotation = 90
    elif (button == pyglet.window.mouse.MIDDLE):
        sprites[0][0].rotation = 0

    return


def move_sprite(x, y):
    myuav = sprites[0][0]
    myuav.pos_x = x
    myuav.pos_y = y
    return

def update_sprite(dt):
    MAX_SPEED = 1
    MAX_ROT_SPEED = 1

    myuav = sprites[0][0]

    lx = sprites[0][1]
    ly = sprites[0][2]

    vel_x = limit((lx - myuav.x) / 20, -MAX_SPEED, MAX_SPEED)
    vel_y = limit((ly - myuav.y) / 20, -MAX_SPEED, MAX_SPEED)

    rot = math.atan2(vel_y, vel_x) * 180 / math.pi - myuav.rotation
    if rot > 180:
        rot -= 360
    elif rot < -180:
        rot += 360

    vel_rot = limit(rot, -MAX_ROT_SPEED, MAX_ROT_SPEED)

    myuav.velocity = (vel_x, vel_y)

    myuav.x = limit(myuav.x + myuav.velocity[0], 0, window.width)
    myuav.y = limit(myuav.y + myuav.velocity[1], 0, window.height)
    myuav.rotation += vel_rot
    return


#pyglet.clock.schedule_interval(update, 1/30.0)
pyglet.clock.schedule_interval(update_sprite, 1 / 30.0)

pyglet.app.run()

