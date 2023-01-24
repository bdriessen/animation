class UXV:
    def __init__(self, name, image):
        self.name = name
        uxv_image = pyglet.resource.image('res/' + image)
        uxv.anchor_x = uav.width // 2
        uav.anchor_y = uav.height // 2
        # sprites are defined as: [sprite, setpoint_x, setpoint_y, setpoint_angle]
        self.sprite = pyglet.sprite.Sprite(uxv, x=window.width / 2, y=window.height / 2)
        self.sp_pos = [0, 0, 0]
        self.sp_vel = [0, 0, 0]
        self.sp_traj = [[]]
        self.mode = "idle"  # idle, pos, vel, traj
        self.label = pyglet.text.Label(self.name,
                                        font_name='Times New Roman', font_size=10,
                                        color=(0, 0, 0, 255),
                                        x=self.sprite.x, y=self.sprite.y - uav.anchor_y, anchor_x='center', anchor_y='center',
                                        multiline=True, width=150)
        self.label.set_style('background_color', (255, 255, 255, 100))
        self.label.set_style('align', 'center')
        self.sprite.scale = 0.15