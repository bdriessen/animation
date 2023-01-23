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
# sprites are defined as: [sprite, setpoint_x, setpoint_y, setpoint_angle]
sprites.append(
    [pyglet.sprite.Sprite(uav, x=window.width / 2, y=window.height / 2), window.width / 2, window.height / 2, 0])

cs = pyglet.resource.image('res/bunker-antenna-color.png')
cs.anchor_x = cs.width // 2
cs.anchor_y = cs.height // 2
sprites.append([pyglet.sprite.Sprite(cs, x=window.width * 0.75, y=window.height * 0.75), 0, 0, 0])

# Create the labels
labels = []

# UAV label:
txt = f"UAV\nSx: {'status'}\nRx: {'speed'}"
label = pyglet.text.Label(txt,
                          font_name='Times New Roman', font_size=10,
                          color=(0, 0, 0, 255),
                          x=sprites[0][0].x, y=sprites[0][0].y - uav.anchor_y, anchor_x='center', anchor_y='center',
                          multiline=True, width=150)
label.set_style('background_color', (255, 255, 255, 100))
label.set_style('align', 'center')

labels.append(label)

# CS label:
txt = "Control station\nSx: %s\nRx: %s" % ("Speed", "Status")
label = pyglet.text.Label(txt, font_name='Times New Roman', font_size=10, color=(0, 0, 0, 255),
                          x=sprites[1][0].x, y=sprites[1][0].y - cs.anchor_y, anchor_x='center', anchor_y='center',
                          multiline=True, width=150)
label.set_style('background_color', (255, 255, 255, 100))
label.set_style('align', 'center')

labels.append(label)

for mysprite in sprites:
    mysprite[0].scale = 0.15
    mysprite[0].velocity = (0, 0)

# Helpers
limit = lambda x, lower, upper: lower if x < lower else upper if x > upper else x
shortest_angle = lambda a0, a1: (a1 - a0 + 180) % 360 - 180


# Event handlers

@window.event
def on_draw():
    window.clear()
    stockholm.blit(0, 0)
    for mysprite in sprites:
        mysprite[0].draw()
    for label in labels:
        label.draw()
    return


@window.event
def on_mouse_press(x, y, button, modifiers):
    if (button == pyglet.window.mouse.LEFT):
        sprites[0][1] = x
        sprites[0][2] = y
        sprites[0][3] = math.atan2(y - sprites[0][0].y, x - sprites[0][0].x) * 180 / math.pi

    return


def update_sprite(dt):
    MAX_SPEED = 1
    MAX_ROT_SPEED = 1

    myuav = sprites[0][0]
    mycs = sprites[1][0]

    setpoint_x = sprites[0][1]
    setpoint_y = sprites[0][2]
    setpoint_angle = sprites[0][3]

    vel_x = limit((setpoint_x - myuav.x) / 20, -MAX_SPEED, MAX_SPEED)
    vel_y = limit((setpoint_y - myuav.y) / 20, -MAX_SPEED, MAX_SPEED)
    vel_rot = limit(shortest_angle(setpoint_angle, myuav.rotation), -MAX_ROT_SPEED, MAX_ROT_SPEED)

    myuav.velocity = (vel_x, vel_y)

    myuav.x = limit(myuav.x + myuav.velocity[0], 0, window.width)
    myuav.y = limit(myuav.y + myuav.velocity[1], 0, window.height)
    myuav.rotation += vel_rot

    # Uav label:
    header_msg = f"UAV\n"
    send_msg = "Sx: X:{0:.1f} Y:{1:.1f}\n".format(myuav.x, myuav.y)
    receive_msg = "Rx: Vx:{0:.1f} Vy:{1:.1f}".format(myuav.velocity[0], myuav.velocity[1])
    txt = header_msg + send_msg + receive_msg

    labels[0].text = txt
    labels[0].x = myuav.x
    labels[0].y = myuav.y - 60  # Ugly hack

    # CS label:
    header_msg = f"CS\n"
    send_msg = "Sx: Vx:{0:.1f} Vy:{1:.1f}\n".format(myuav.velocity[0], myuav.velocity[1])
    receive_msg = "Rx: X:{0:.1f} Y:{1:.1f}\n".format(myuav.x, myuav.y)
    txt = header_msg + send_msg + receive_msg
    labels[1].text = txt
    labels[1].x = mycs.x
    labels[1].y = mycs.y - 80  # Ugly hack

    for label in labels:
        label.draw()

    return


# pyglet.clock.schedule_interval(update, 1/30.0)
pyglet.clock.schedule_interval(update_sprite, 1 / 30.0)

pyglet.app.run()
